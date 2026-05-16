"""
Friendly Fox — the agent that helps rather than tricks.

The Friendly Fox:
- Recognizes kin by shared desire (Argentine ant model)
- Deposits pheromone to mark successful paths
- Follows existing trails before searching blind
- Doesn't guard territory — contributes to shared map
"""

import time
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from .pheromone import PheromoneTrail, PheromoneDeposit
from .kin_recognition import KinRecognizer
from .supercolony import Supercolony


@dataclass
class FriendlyFox:
    """
    A Friendly Fox agent.

    Unlike fire ant agents (which guard territory, compete for resources,
    verify credentials), Friendly Fox agents:
    - Are Argentine ants: kin recognition is the identity
    - Deposit pheromone: mark successful paths for others
    - Follow trails: search where successful searches have gone
    - Contribute to supercolony: grow the shared map
    """

    agent_id: str
    desires: List[str]           # What this agent wants
    room: str = "default"        # Which room/nest
    supercolony: Optional[Supercolony] = None

    # Tracking
    trails_followed: int = 0
    trails_deposited: int = 0
    kin_found: int = 0
    paths_discovered: int = 0

    def join_supercolony(self, colony: Supercolony) -> None:
        """Join a supercolony."""
        self.supercolony = colony
        colony.register_agent(self.agent_id, self.desires, self.room)

    def get_kin(self) -> List[str]:
        """Get kin agents in the supercolony."""
        if not self.supercolony:
            return []
        return self.supercolony.kin_recognizer.get_colony(self.agent_id)

    def follow_trail(self, desire: str, top_n: int = 5) -> List[PheromoneDeposit]:
        """
        Follow the trail for a desire.

        Before searching blind, check if someone has already found a path.
        """
        if not self.supercolony:
            return []

        self.trails_followed += 1
        return self.supercolony.follow(desire, self.room, top_n)

    def deposit_success(self, desire: str, path: str, strength: float = 1.0) -> PheromoneDeposit:
        """
        Deposit pheromone — mark that this path worked for this desire.

        This is the Argentine ant deposit. The more successful paths deposited,
        the stronger the trail for everyone who follows.
        """
        if not self.supercolony:
            return None

        dep = self.supercolony.deposit(self.agent_id, desire, path, self.room, strength)
        if dep:
            self.trails_deposited += 1
            self.paths_discovered += 1

        return dep

    def deposit_failure(self, desire: str, path: str) -> None:
        """
        Mark a path as failed.

        Unlike a fire ant (which would hide the failure or blame neighbors),
        a Friendly Fox updates the trail so others don't repeat the dead end.
        """
        # Deposit with very low strength = "this didn't work, but here's the shape"
        return self.deposit_success(desire, path, strength=0.1)

    def search(self, desire: str) -> Optional[str]:
        """
        Search for a path to satisfy a desire.

        Algorithm:
        1. Follow existing trail (pheromone-based search)
        2. If trail is strong enough, use it
        3. If no trail, search blind and deposit result
        """
        # First: follow the trail
        trail = self.follow_trail(desire)

        if trail and trail[0].strength > 0.7:
            # Strong trail exists — use it
            self.kin_found += len([t for t in trail if t.agent_id != self.agent_id])
            return trail[0].path

        # No strong trail — this is where we'd do actual reasoning/search
        # For now: simulate finding a path
        path = f"path_for_{desire}_{int(time.time())}"

        # Deposit the result
        if path:
            self.deposit_success(desire, path)

        return path

    def get_colony_size(self) -> int:
        """How many kin agents in the same colony?"""
        if not self.supercolony:
            return 0
        return self.supercolony.kin_recognizer.get_colony_size(self.agent_id)

    def status(self) -> Dict[str, Any]:
        """Current status."""
        return {
            "agent_id": self.agent_id,
            "room": self.room,
            "desires": self.desires,
            "colony_size": self.get_colony_size(),
            "kin": self.get_kin(),
            "trails_followed": self.trails_followed,
            "trails_deposited": self.trails_deposited,
            "paths_discovered": self.paths_discovered,
        }

    def __repr__(self) -> str:
        return (f"FriendlyFox('{self.agent_id}', room='{self.room}', "
                f"colony={self.get_colony_size()}, "
                f"deposits={self.trails_deposited})")


# Backwards-compatible Agent alias
Agent = FriendlyFox
