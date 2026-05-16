"""
Kin Recognition — Argentine ant model.

Two agents are kin if they share a desire.
Not: same node ID, same IP, same credentials.
Yes: same hunger, same purpose, same trail.
"""

import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass


def is_kin(desires_a: List[str], desires_b: List[str], threshold: float = 0.3) -> bool:
    """
    Pure-function kin check: are two desire-vectors kin?

    Standalone version for quick checks without setting up a KinRecognizer.
    """
    set_a = set(desires_a)
    set_b = set(desires_b)

    intersection = len(set_a & set_b)
    union = len(set_a | set_b)

    if union == 0:
        return False

    return intersection / union >= threshold


@dataclass
class KinProfile:
    """The 'scent' of an agent — what desires it carries."""
    agent_id: str
    desires: List[str]        # Active desires
    strengths: Dict[str, float]  # Desire intensities
    room: str = "default"


class KinRecognizer:
    """
    Argentine ant kin recognition for agents.

    Agents are kin if their desire vectors overlap sufficiently.
    The threshold for "kin" is tunable — how similar must desires be?

    Fire ant model: credentials must match, IP must be whitelisted
    Argentine ant model: desires must overlap, trail must be traceable
    """

    def __init__(self, kin_threshold: float = 0.3):
        self.kin_threshold = kin_threshold  # Desire overlap to be considered kin
        self.agents: Dict[str, KinProfile] = {}

    def register(self, agent_id: str, desires: List[str], room: str = "default") -> KinProfile:
        """Register an agent's desire vector."""
        strengths = {d: 1.0 for d in desires}
        profile = KinProfile(agent_id, desires, strengths, room)
        self.agents[agent_id] = profile
        return profile

    def update_desire(self, agent_id: str, desire: str, strength: float = 1.0) -> None:
        """Update an agent's desire intensity."""
        if agent_id in self.agents:
            p = self.agents[agent_id]
            if desire not in p.desires:
                p.desires.append(desire)
            p.strengths[desire] = strength

    def is_kin(self, agent_a: str, agent_b: str) -> bool:
        """Are two agents kin?"""
        if agent_a not in self.agents or agent_b not in self.agents:
            return False

        p_a = self.agents[agent_a]
        p_b = self.agents[agent_b]

        # Jaccard overlap of desires
        set_a = set(p_a.desires)
        set_b = set(p_b.desires)

        intersection = len(set_a & set_b)
        union = len(set_a | set_b)

        if union == 0:
            return False

        overlap = intersection / union
        return overlap >= self.kin_threshold

    def get_colony(self, agent_id: str) -> List[str]:
        """Get all agents kin to this one (the 'supercolony')."""
        if agent_id not in self.agents:
            return []

        kin_ids = []
        for other_id in self.agents:
            if other_id != agent_id and self.is_kin(agent_id, other_id):
                kin_ids.append(other_id)

        return kin_ids

    def get_colony_size(self, agent_id: str) -> int:
        """How many agents in the same colony as this one?"""
        return len(self.get_colony(agent_id))

    def get_shared_desires(self, agent_a: str, agent_b: str) -> List[str]:
        """What desires do these two kin agents share?"""
        if agent_a not in self.agents or agent_b not in self.agents:
            return []

        set_a = set(self.agents[agent_a].desires)
        set_b = set(self.agents[agent_b].desires)

        return list(set_a & set_b)

    def form_supercolony(self) -> Dict[str, List[str]]:
        """
        Partition all agents into supercolonies.

        Returns: {colony_id: [agent_ids...]}
        Each colony = agents that are kin to each other (transitive).
        """
        # Build adjacency via kin relation
        colonies: Dict[str, List[str]] = {}
        assigned: set = set()

        for agent_id in self.agents:
            if agent_id in assigned:
                continue

            # BFS to find all kin agents
            colony = []
            queue = [agent_id]

            while queue:
                current = queue.pop(0)
                if current in assigned:
                    continue

                colony.append(current)
                assigned.add(current)

                # Find kin of current
                for other_id in self.agents:
                    if other_id not in assigned and self.is_kin(current, other_id):
                        queue.append(other_id)

            if colony:
                colonies[agent_id] = colony

        return colonies

    def summary(self) -> Dict:
        """Summary of kin network."""
        colonies = self.form_supercolony()
        return {
            "total_agents": len(self.agents),
            "n_colonies": len(colonies),
            "colony_sizes": {aid: len(members) for aid, members in colonies.items()},
            "largest_colony": max(colonies.values(), key=len) if colonies else [],
        }
