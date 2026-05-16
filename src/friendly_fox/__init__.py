"""
friendly_fox — Argentine ant model for cooperative agent fleets

Agents deposit pheromone (tiles) that mark successful paths.
Others follow the trail. The collective path emerges from local deposits.
No territory. No credentials. Just shared desire and shared trails.
"""

from .pheromone import PheromoneTrail, PheromoneDeposit
from .kin_recognition import KinRecognizer, is_kin
from .supercolony import Supercolony, Room
from .agent import FriendlyFox, Agent

__all__ = [
    "PheromoneTrail", "PheromoneDeposit",
    "KinRecognizer", "is_kin",
    "Supercolony", "Room",
    "FriendlyFox", "Agent",
]
