"""
Supercolony — agents that are kin via shared desire.

A supercolony is not a team. A team is assigned.
A supercolony is recognized. Agents find each other by scent.
"""

import time
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
from .pheromone import PheromoneTrail, PheromoneDeposit
from .kin_recognition import KinRecognizer, KinProfile


@dataclass
class Room:
    """A room/nest in the supercolony."""
    name: str
    purpose: str              # What this room is FOR (not what's IN it)
    agents: List[str] = field(default_factory=list)
    pheromone_trail: PheromoneTrail = field(default_factory=PheromoneTrail)
    birth_time: float = field(default_factory=time.time)

    def deposit(self, desire: str, path: str, agent_id: str, strength: float = 1.0) -> PheromoneDeposit:
        """Deposit pheromone in this room."""
        return self.pheromone_trail.deposit(desire, path, agent_id, self.name, strength)

    def follow(self, desire: str, top_n: int = 5) -> List[PheromoneDeposit]:
        """Follow this room's trail for a desire."""
        return self.pheromone_trail.follow(desire, self.name, top_n)


class Supercolony:
    """
    The supercolony — one fleet stretched across rooms.

    Unlike a team, which is defined by assignment,
    a supercolony is defined by kin recognition.
    Agents are kin if they share a desire.

    The supercolony has:
    - Rooms (nests)
    - Agents registered to rooms
    - Kin recognition (shared desire → kin)
    - Pheromone trails (successful paths)
    - Cross-room invariants (paths that work everywhere)

    The supercolony grows around shared desire.
    When a new desire emerges, new kin recognize each other and form a new sub-colony.
    """

    def __init__(self, name: str = "default"):
        self.name = name
        self.rooms: Dict[str, Room] = {}
        self.kin_recognizer = KinRecognizer()
        self.global_trail = PheromoneTrail()  # Trail across all rooms
        self.cross_room_invariants: List[PheromoneDeposit] = []

    def add_room(self, name: str, purpose: str) -> Room:
        """Add a room/nest to the supercolony."""
        room = Room(name=name, purpose=purpose)
        self.rooms[name] = room
        return room

    def register_agent(self, agent_id: str, desires: List[str], room: str = "default") -> KinProfile:
        """Register an agent in a room."""
        if room not in self.rooms:
            self.add_room(room, purpose=f"Room {room}")

        self.rooms[room].agents.append(agent_id)
        return self.kin_recognizer.register(agent_id, desires, room)

    def deposit(self, agent_id: str, desire: str, path: str, room: str = "default",
                strength: float = 1.0) -> PheromoneDeposit:
        """Deposit pheromone — mark a successful path."""
        if room not in self.rooms:
            return None

        # Deposit in the room
        dep = self.rooms[room].deposit(desire, path, agent_id, strength)

        # Also add to global trail
        self.global_trail.deposit(desire, path, agent_id, room, strength)

        return dep

    def follow(self, desire: str, room: str = None, top_n: int = 5) -> List[PheromoneDeposit]:
        """Follow the trail for a desire."""
        if room and room in self.rooms:
            return self.rooms[room].follow(desire, top_n)
        return self.global_trail.follow(desire, top_n=top_n)

    def find_cross_room_invariants(self, desire: str) -> List[PheromoneDeposit]:
        """
        Find paths that work across MULTIPLE rooms.
        These are the structure — the cross-plane invariants.

        Invariant path = successfully followed in ≥2 rooms for the same desire.
        """
        return self.global_trail.find_invariant(desire)

    def get_colony_report(self) -> Dict[str, Any]:
        """Get a report on the supercolony's structure."""
        kin_summary = self.kin_recognizer.summary()
        colonies = kin_summary.get("colony_sizes", {})

        room_summaries = {}
        for name, room in self.rooms.items():
            room_summaries[name] = {
                "purpose": room.purpose,
                "n_agents": len(room.agents),
                "n_deposits": len(room.pheromone_trail),
                "desires_tracked": len(set(d.desire for d in room.pheromone_trail.deposits if d.alive)),
            }

        return {
            "supercolony": self.name,
            "n_rooms": len(self.rooms),
            "kin": kin_summary,
            "cross_room_invariants": len(self.cross_room_invariants),
            "rooms": room_summaries,
        }

    def summary(self) -> str:
        r = self.get_colony_report()
        return (f"Supercolony '{r['supercolony']}': "
                f"{r['n_rooms']} rooms, "
                f"{r['kin']['total_agents']} agents, "
                f"{r['kin']['n_colonies']} colonies, "
                f"{r['cross_room_invariants']} cross-room invariants")
