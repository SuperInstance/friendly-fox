"""
Pheromone — tiles that mark successful paths.

A pheromone deposit carries:
- desire: what this path was trying to satisfy
- path: what worked (abstraction, connection, result)
- strength: how confident (evaporates over time)
- agent: who deposited it (for trail tracing)
- room: which room it was deposited in
"""

import time
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import numpy as np


@dataclass
class PheromoneDeposit:
    """A single pheromone deposit — a tile marking a successful path."""
    desire: str                    # The desire this path satisfies
    path: str                      # What worked (abstraction/connection)
    strength: float = 1.0          # Initial strength (evaporates over time)
    agent_id: str = "unknown"      # Who deposited it
    room: str = "default"          # Which room/nest
    timestamp: float = field(default_factory=time.time)
    evaporation_rate: float = 0.01  # Strength lost per unit time
    deposit_id: str = field(default_factory=lambda: f"dep_{int(time.time()*1000)}")

    def evaporate(self, dt: float) -> None:
        """Reduce strength over time."""
        self.strength = max(0.0, self.strength - self.evaporation_rate * dt)

    @property
    def alive(self) -> bool:
        """Is this deposit still potent enough to follow?"""
        return self.strength > 0.05


class PheromoneTrail:
    """
    A trail of pheromone deposits.

    Agents follow the strongest deposits for a given desire.
    Deposits evaporate over time — successful paths must be re-deposited.

    The trail is the map. No single agent knows the whole picture.
    """

    def __init__(self, evaporation_rate: float = 0.01):
        self.deposits: List[PheromoneDeposit] = []
        self.evaporation_rate = evaporation_rate
        self.room_trails: Dict[str, List[PheromoneDeposit]] = {}  # Per-room trails
        self.global_trail: List[PheromoneDeposit] = []  # Across all rooms

    def deposit(self, desire: str, path: str, agent_id: str, room: str = "default",
                strength: float = 1.0) -> PheromoneDeposit:
        """Deposit pheromone — mark a successful path for a desire."""
        dep = PheromoneDeposit(
            desire=desire,
            path=path,
            strength=strength,
            agent_id=agent_id,
            room=room,
            evaporation_rate=self.evaporation_rate
        )
        self.deposits.append(dep)

        # Add to room-specific trail
        if room not in self.room_trails:
            self.room_trails[room] = []
        self.room_trails[room].append(dep)

        # Add to global trail
        self.global_trail.append(dep)

        return dep

    def follow(self, desire: str, room: str = None, top_n: int = 5) -> List[PheromoneDeposit]:
        """
        Follow the trail for a desire.

        Returns the top_n strongest deposits matching this desire.
        If room is specified, search only in that room's trail.
        """
        if room and room in self.room_trails:
            candidates = [d for d in self.room_trails[room] if d.alive and desire.lower() in d.desire.lower()]
        else:
            candidates = [d for d in self.deposits if d.alive and desire.lower() in d.desire.lower()]

        # Sort by strength descending
        candidates.sort(key=lambda d: d.strength, reverse=True)
        return candidates[:top_n]

    def evaporate_all(self, dt: float) -> int:
        """Evaporate all deposits. Returns number of deposits that died."""
        dead = 0
        for dep in self.deposits:
            dep.evaporate(dt)
            if not dep.alive:
                dead += 1
        return dead

    def get_trail_summary(self, desire: str) -> Dict[str, Any]:
        """Get a summary of the trail for a desire."""
        deposits = [d for d in self.deposits if desire.lower() in d.desire.lower()]
        if not deposits:
            return {"total": 0, "alive": 0, "avg_strength": 0.0, "agents": []}

        alive = [d for d in deposits if d.alive]
        return {
            "total": len(deposits),
            "alive": len(alive),
            "avg_strength": np.mean([d.strength for d in alive]) if alive else 0.0,
            "agents": list(set(d.agent_id for d in deposits)),
            "rooms": list(set(d.room for d in deposits)),
            "top_paths": [d.path for d in sorted(alive, key=lambda x: x.strength, reverse=True)[:3]]
        }

    def find_invariant(self, desire: str) -> List[PheromoneDeposit]:
        """
        Find invariants — deposits that appear across MULTIPLE rooms for the same desire.
        These are the structure in the randomness (cross-plane invariants).
        """
        deposits = [d for d in self.deposits if d.alive and desire.lower() in d.desire.lower()]
        if len(deposits) < 2:
            return []

        # Group by path
        path_rooms: Dict[str, set] = {}
        for d in deposits:
            if d.path not in path_rooms:
                path_rooms[d.path] = set()
            path_rooms[d.path].add(d.room)

        # Invariant = same path across multiple rooms
        invariants = []
        for path, rooms in path_rooms.items():
            if len(rooms) > 1:
                # Find the deposits for this invariant path
                for d in deposits:
                    if d.path == path:
                        invariants.append(d)
                        break

        return invariants

    def __len__(self) -> int:
        return len(self.deposits)

    def __repr__(self) -> str:
        alive = sum(1 for d in self.deposits if d.alive)
        return f"PheromoneTrail({len(self)} deposits, {alive} alive)"
