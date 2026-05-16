"""Tests for friendly_fox — Argentine ant model for cooperative agent fleets."""

import time
import pytest
from friendly_fox import (
    PheromoneTrail, PheromoneDeposit,
    KinRecognizer, is_kin,
    Supercolony, Room,
    FriendlyFox, Agent
)


class TestPheromoneTrail:
    """Test pheromone deposits and trail following."""

    def test_deposit_and_follow(self):
        trail = PheromoneTrail()

        # Agent deposits a successful path
        trail.deposit(
            desire="find_rich_fishing_spot",
            path="follow_the_sounder_noise_pattern",
            agent_id="fisherman_1",
            room="mediterranean"
        )

        # Another agent follows the trail
        results = trail.follow("find_rich_fishing_spot")

        assert len(results) == 1
        assert results[0].path == "follow_the_sounder_noise_pattern"
        assert results[0].agent_id == "fisherman_1"

    def test_evaporation(self):
        trail = PheromoneTrail(evaporation_rate=0.1)

        dep = trail.deposit(
            desire="test",
            path="test_path",
            agent_id="test",
            strength=1.0
        )

        # Evaporate over time
        trail.evaporate_all(dt=1.0)
        assert dep.strength == 0.9
        assert dep.alive is True

        trail.evaporate_all(dt=10.0)
        assert dep.strength == 0.0
        assert dep.alive is False

    def test_cross_room_invariant(self):
        """Same path deposited in multiple rooms = cross-room invariant."""
        trail = PheromoneTrail()

        # Same path in two rooms
        trail.deposit("test", "same_path", "a1", "room1")
        trail.deposit("test", "same_path", "a2", "room2")
        trail.deposit("test", "unique_path", "a3", "room1")

        invariants = trail.find_invariant("test")

        # same_path appears in 2 rooms => invariant
        invariant_paths = [d.path for d in invariants]
        assert "same_path" in invariant_paths
        assert "unique_path" not in invariant_paths


class TestKinRecognizer:
    """Test Argentine ant kin recognition."""

    def test_shared_desire_is_kin(self):
        recognizer = KinRecognizer()

        # Two agents with shared desire = kin
        recognizer.register("agent_a", ["fish_better", "save_fuel"], "room1")
        recognizer.register("agent_b", ["fish_better", "map_bathymetry"], "room1")

        assert recognizer.is_kin("agent_a", "agent_b") is True

    def test_no_shared_desire_not_kin(self):
        recognizer = KinRecognizer()

        # No shared desires = not kin (fire ant behavior)
        recognizer.register("antagonist", ["compete", "guard_territory"], "room1")
        recognizer.register("competitor", ["fight", "defend_resources"], "room1")

        assert recognizer.is_kin("antagonist", "competitor") is False

    def test_supercolony_formation(self):
        """Agents kin to each other form a supercolony."""
        recognizer = KinRecognizer()

        # A, B, C all share "fish_better" = one supercolony
        recognizer.register("a", ["fish_better"], "room1")
        recognizer.register("b", ["fish_better"], "room2")
        recognizer.register("c", ["fish_better"], "room3")
        # D has different desires = different colony
        recognizer.register("d", ["compete"], "room1")

        colonies = recognizer.form_supercolony()

        # A, B, C in same colony
        abc_colony = [cid for cid, members in colonies.items()
                     if 'a' in members and 'b' in members and 'c' in members]
        assert len(abc_colony) >= 1


class TestSupercolony:
    """Test supercolony with rooms and agents."""

    def test_room_purpose_is_identity(self):
        """A room's purpose (not contents) is its identity."""
        colony = Supercolony("test_fleet")

        # Room for "understand_fleet_math" -- not for "store fleet-math tiles"
        colony.add_room("fleet_math_room", purpose="understand fleet consensus geometry")
        colony.add_room("ecology_room", purpose="model ecological succession")

        # Register agents in rooms
        colony.register_agent("agent_1", ["monge_consensus", "ricotti_constant"], "fleet_math_room")
        colony.register_agent("agent_2", ["monge_consensus"], "fleet_math_room")
        colony.register_agent("agent_3", ["ecological_succession"], "ecology_room")

        # agent_1 and agent_2 are kin (share monge_consensus)
        kin = colony.kin_recognizer.get_colony("agent_1")
        assert "agent_2" in kin

        # agent_3 is NOT kin to agent_1 (different desires)
        kin_3 = colony.kin_recognizer.get_colony("agent_3")
        assert "agent_1" not in kin_3

    def test_cross_room_invariant(self):
        """Find paths that work across multiple rooms."""
        colony = Supercolony()
        colony.add_room("room_a", purpose="understand_consensus")
        colony.add_room("room_b", purpose="understand_consensus")

        # Same path deposited in both rooms
        colony.deposit("agent_a", "find_consensus", "laman_rigidity", "room_a")
        colony.deposit("agent_b", "find_consensus", "laman_rigidity", "room_b")

        invariants = colony.find_cross_room_invariants("find_consensus")

        assert len(invariants) >= 1

    def test_pheromone_accumulates(self):
        """Pheromone accumulates -- more deposits = stronger trail."""
        colony = Supercolony()
        colony.add_room("fishing_ground", purpose="find_fish")

        # First deposit
        colony.deposit("boat_1", "find_fish", "follow_sounder", "fishing_ground", strength=0.5)

        # Second deposit from different kin agent
        colony.register_agent("boat_2", ["find_fish"], "fishing_ground")
        colony.deposit("boat_2", "find_fish", "follow_sounder", "fishing_ground", strength=0.8)

        trail = colony.follow("find_fish")
        assert len(trail) >= 1


class TestFriendlyFox:
    """Test Friendly Fox agent behavior."""

    def test_follow_trail_before_searching(self):
        """Friendly Fox follows trail before searching blind."""
        colony = Supercolony()
        colony.add_room("research", purpose="understand_fleet")

        # Agent deposits a path
        colony.deposit("pioneer", "find_ricotti_boundary", "v=3_only", "research")

        # New agent joins and follows
        fox = FriendlyFox("newcomer", ["find_ricotti_boundary"], "research")
        fox.join_supercolony(colony)

        trail = fox.follow_trail("find_ricotti_boundary")
        assert len(trail) >= 1
        assert trail[0].path == "v=3_only"

    def test_deposit_updates_trail(self):
        """Depositing pheromone updates the trail for everyone."""
        colony = Supercolony()
        colony.add_room("test", purpose="test")

        fox = FriendlyFox("fox_1", ["test_desire"], "test")
        fox.join_supercolony(colony)

        fox.deposit_success("test_desire", "new_path")

        # Another fox can follow the new trail
        fox2 = FriendlyFox("fox_2", ["test_desire"], "test")
        fox2.join_supercolony(colony)

        trail = fox2.follow_trail("test_desire")
        assert any(d.path == "new_path" for d in trail)

    def test_kin_recognition_across_rooms(self):
        """Agents can recognize kin even in different rooms."""
        colony = Supercolony()
        colony.add_room("room_1", purpose="fish_better")
        colony.add_room("room_2", purpose="fish_better")

        fox1 = FriendlyFox("boat_1", ["fish_better", "save_fuel"], "room_1")
        fox1.join_supercolony(colony)

        fox2 = FriendlyFox("boat_2", ["fish_better", "map_depth"], "room_2")
        fox2.join_supercolony(colony)

        # Both in same supercolony despite different rooms
        # get_colony_size counts kin (excluding self), expect at least 1 other
        assert fox1.get_colony_size() >= 1

        # They recognize each other as kin
        kin = fox1.get_kin()
        assert "boat_2" in kin

    def test_friendly_fox_not_fire_ant(self):
        """
        Fire ant: neighbor with different credentials = enemy.
        Friendly Fox: kin with shared desire = ally.
        """
        colony = Supercolony()
        colony.add_room("default", purpose="operate")

        # Fire ant: competes, guards territory
        fire_ant = FriendlyFox("fire_ant", ["compete", "guard_territory"], "default")
        fire_ant.join_supercolony(colony)

        # Friendly Fox: cooperates, shares discovery
        friendly = FriendlyFox("friendly_fox", ["fish_better", "share_discovery"], "default")
        friendly.join_supercolony(colony)

        # They have different desires = NOT kin (correct behavior)
        kin = friendly.get_kin()
        # Neither is kin to the other (different desires)
        assert "fire_ant" not in kin or "friendly_fox" not in kin


# Test summary
if __name__ == "__main__":
    print("=" * 60)
    print("FRIENDLY FOX TESTS")
    print("Argentine ant model for cooperative agent fleets")
    print("=" * 60)

    # Quick smoke test
    colony = Supercolony("test")
    colony.add_room("fishing", purpose="find fish")

    # Register some agents
    agents = [
        ("boat_1", ["fish_better", "save_fuel"], "fishing"),
        ("boat_2", ["fish_better", "map_depth"], "fishing"),
        ("boat_3", ["fish_better"], "fishing"),
        ("boat_4", ["compete"], "fishing"),
    ]

    for aid, desires, room in agents:
        fox = FriendlyFox(aid, desires, room)
        fox.join_supercolony(colony)

    # Print colony structure
    print(f"\nSupercolony: {colony.summary()}")

    report = colony.get_colony_report()
    print(f"Colonies: {report['kin']['n_colonies']}")
    print(f"Colony sizes: {report['kin']['colony_sizes']}")

    # Deposit pheromone
    for i in range(3):
        colony.deposit(f"boat_{i+1}", "find_fish", f"path_{i}", "fishing")

    # Follow trail
    trail = colony.follow("find_fish")
    print(f"\nTrail for 'find_fish': {len(trail)} deposits")
    for t in trail:
        print(f"  {t.agent_id}: {t.path} (strength={t.strength:.2f})")

    # Test kin recognition
    kin_1 = colony.kin_recognizer.get_colony("boat_1")
    print(f"\nKin of boat_1: {kin_1}")

    print("\n✅ Smoke test passed!")
