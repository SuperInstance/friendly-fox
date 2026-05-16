# friendly-fox ⚒️🦊

**Argentine ant model for cooperative agent fleets.**

No credentials. No territory. Just shared desire and shared trails.

Friendly Fox agents behave like Argentine ants — they recognize kin by shared desire, mark successful paths with pheromone deposits, and form supercolonies spanning rooms. The result is swarm intelligence that outperforms isolated optimizers.

## Install

```bash
# From PyPI (coming soon)
# pip install friendly-fox

# From source (current)
git clone https://github.com/SuperInstance/friendly-fox.git
cd friendly-fox
pip install -e .
```

### Requirements

- Python ≥ 3.10
- NumPy (for averaging pheromone strength)

## Quick Start

```python
from friendly_fox import Supercolony, FriendlyFox

# 1. Create a supercolony — one fleet stretched across rooms
colony = Supercolony("fishing_fleet")
colony.add_room("mediterranean", purpose="find fish")
colony.add_room("atlantic", purpose="find fish")

# 2. Agents join by shared desire, not credentials
fox_1 = FriendlyFox("boat_1", ["fish_better", "save_fuel"], "mediterranean")
fox_1.join_supercolony(colony)

fox_2 = FriendlyFox("boat_2", ["fish_better", "map_depth"], "atlantic")
fox_2.join_supercolony(colony)

fox_3 = FriendlyFox("boat_3", ["compete", "guard_territory"], "mediterranean")
fox_3.join_supercolony(colony)

# 3. Deposit pheromone — mark a successful path
fox_1.deposit_success("fish_better", "follow_sounder_pattern_near_rock")

# 4. Follow the trail — don't search blind
trail = fox_2.follow_trail("fish_better")
print(f"Found {len(trail)} paths from kin")  # 1 path from boat_1

# 5. Compare supercolony membership
print(f"fox_1 colony size: {fox_1.get_colony_size()}")   # 1 (has kin with boat_2)
print(f"fox_3 colony size: {fox_3.get_colony_size()}")   # 0 (no shared desires)
```

## How It Works

### The Argentine Ant Metaphor

**Fire ants** fight kin from neighboring nests. They guard territory individually. The system optimizes for individual survival at the cost of collective scale.

**Argentine ants** don't fight across nests. They recognize kin by shared chemistry across continents. Each ant deposits a little pheromone, follows a little, and the collective path emerges from local decisions. This lets them form the largest known animal societies on Earth — supercolonies spanning continents.

**Friendly Fox** applies this model to agents:

1. **Kin recognition is identity.** Two agents are kin if their desire vectors overlap (Jaccard similarity ≥ 0.3). Not node ID, not IP address, not credentials — just shared desire.

2. **The trail is the map.** No single agent knows the whole picture. Pheromone deposits from individual agents accumulate into a collective trail. Agents follow existing trails before searching blind.

3. **Evaporation prevents stagnation.** Old deposits fade over time. Successful paths must be re-deposited, or the trail vanishes. This is the ant colony optimization analog — it prevents dead-end paths from persisting forever.

4. **Supercolonies form around shared desire.** Agents contributing to the same purpose naturally form a supercolony — one fleet stretched across multiple rooms. The supercolony isn't assigned; it's recognized.

5. **Cross-room invariants** are paths that work across multiple rooms for the same desire. These are the structure in the randomness — patterns that hold regardless of context.

### Fire Ant vs Friendly Fox

| | Fire Ant | Argentine Ant (Friendly Fox) |
|---|---|---|
| **Neighbor from same fleet** | Fight | Merge |
| **New agent joins** | Vet credentials | Follow trail, deposit pheromone |
| **Path found** | Guard territory | Share discovery |
| **Something fails** | Blame neighbor | Update trail, move on |
| **Scale** | Fragments into territories | Grows supercolony |

## Module Reference

### `pheromone.py` — PheromoneTrail, PheromoneDeposit

The pheromone system. Agents deposit tiles marking successful paths. Deposits carry a `desire`, `path`, `strength`, `agent_id`, and `room`. Strength evaporates over time.

```python
from friendly_fox import PheromoneTrail

trail = PheromoneTrail(evaporation_rate=0.01)

# Deposit a successful path
trail.deposit("find_fish", "follow_sounder", agent_id="boat_1", room="mediterranean")

# Follow the trail for a desire
results = trail.follow("find_fish", top_n=5)

# Evaporate old deposits (call periodically)
trail.evaporate_all(dt=1.0)

# Find cross-room invariants
invariants = trail.find_invariant("find_fish")

# Get trail summary
summary = trail.get_trail_summary("find_fish")
```

Key features:
- Per-room trails + global cross-room trail
- Evaporation prevents stagnation
- Invariant detection (same path across multiple rooms)
- Trail summaries with average strength, agents, rooms

### `kin_recognition.py` — KinRecognizer, is_kin

Jaccard-based desire overlap. Two agents are kin if `|A ∩ B| / |A ∪ B| ≥ 0.3`.

```python
from friendly_fox import KinRecognizer, is_kin

# Quick standalone check
are_kin = is_kin(["fish_better", "save_fuel"], ["fish_better", "map_depth"])
print(are_kin)  # True

# Full registry with colony formation
kin = KinRecognizer(kin_threshold=0.3)
kin.register("agent_a", ["fish_better", "save_fuel"])
kin.register("agent_b", ["fish_better", "map_depth"])

# Check kin relationship
print(kin.is_kin("agent_a", "agent_b"))  # True

# Build supercolonies from all agents
colonies = kin.form_supercolony()
# Returns: {"agent_a": ["agent_a", "agent_b"]}

# Get colony report
report = kin.summary()
```

Key features:
- Pure-function standalone `is_kin()` for quick checks
- Full `KinRecognizer` registry with profiles
- BFS-based supercolony partitioning
- Threshold-tunable (0.3 default)

### `supercolony.py` — Supercolony, Room

One fleet stretched across rooms. The supercolony manages rooms, agents, pheromone trails, and cross-room invariant tracking.

```python
from friendly_fox import Supercolony

colony = Supercolony(name="research_fleet")

# Add rooms
colony.add_room("fleet_math", purpose="understand consensus geometry")
colony.add_room("ecology", purpose="model ecological succession")

# Register agents
colony.register_agent("agent_1", ["monge_consensus"], "fleet_math")
colony.register_agent("agent_2", ["monge_consensus"], "fleet_math")

# Deposit across rooms
colony.deposit("agent_1", "find_consensus", "laman_rigidity", "fleet_math")

# Follow trails
trail = colony.follow("find_consensus", room="fleet_math")

# Find cross-room invariants
invariants = colony.find_cross_room_invariants("find_consensus")

# Get colony report
report = colony.get_colony_report()
```

Key features:
- Room → purpose identity model (rooms defined by purpose, not contents)
- Per-room and global pheromone trails
- Cross-room invariant detection
- Full colony reporting

### `agent.py` — FriendlyFox, Agent

The Friendly Fox agent. Argentine ant behavior: deposits pheromone, follows trails, recognizes kin.

```python
from friendly_fox import FriendlyFox

colony = Supercolony("test")

fox = FriendlyFox(
    agent_id="fox_1",
    desires=["fish_better", "save_fuel"],
    room="mediterranean"
)
fox.join_supercolony(colony)

# Follow before searching blind
trail = fox.follow_trail("fish_better")

# Deposit successes (strengthen trail)
fox.deposit_success("fish_better", "follow_sounder")

# Mark failures too (with low strength)
fox.deposit_failure("fish_better", "chase_random_signals")

# Smart search: follow trail if strong, otherwise explore
path = fox.search("fish_better")

# Check status
print(fox.status())
```

Key features:
- `follow_trail()` — search existing pheromone before blind search
- `deposit_success()` — strengthen the collective trail
- `deposit_failure()` — mark dead ends at low strength
- `search()` — hybrid algorithm: trail → explore → deposit
- `get_kin()` / `get_colony_size()` — supercolony awareness

## Full Examples

### Multi-Agent Swarm Intelligence

```python
from friendly_fox import Supercolony, FriendlyFox

# Build a fleet
colony = Supercolony("tuna_fleet")
colony.add_room("bridge", purpose="navigate")
colony.add_room("deck", purpose="process_catch")

# Launch agents with overlapping desires
crew = [
    ("captain",   ["navigate", "find_fish", "save_fuel"], "bridge"),
    ("navigator", ["navigate", "map_currents"],           "bridge"),
    ("spotter",   ["find_fish", "save_fuel"],             "deck"),
    ("processor", ["process_catch", "quality"],            "deck"),
]

agents = {}
for aid, desires, room in crew:
    agents[aid] = FriendlyFox(aid, desires, room)
    agents[aid].join_supercolony(colony)

# Captain finds a path and deposits pheromone
agents["captain"].deposit_success("find_fish", "follow_thermal_front")

# Spotter follows the trail (doesn't search blind)
trail = agents["spotter"].follow_trail("find_fish")
print(f"Spotter found {len(trail)} trails for 'find_fish'")

# Check who's kin
for aid in ["captain", "navigator", "spotter"]:
    kin_list = agents[aid].get_kin()
    print(f"{aid}: kin = {kin_list}")

# Get colony status
print(agents["captain"].status())
print(colony.summary())
```

### Cross-Room Invariants

```python
from friendly_fox import Supercolony

colony = Supercolony("research")
colony.add_room("room_a", purpose="find patterns")
colony.add_room("room_b", purpose="find patterns")

# Same pattern discovered independently in two rooms
colony.deposit("alice", "find_pattern", "ricotti_boundary_at_v3", "room_a")
colony.deposit("bob",   "find_pattern", "ricotti_boundary_at_v3", "room_b")

# Cross-room invariant detected!
invariants = colony.find_cross_room_invariants("find_pattern")
print(f"Found {len(invariants)} invariants")  # 1
for inv in invariants:
    print(f"  Invariant path: {inv.path} (rooms: {inv.room}+)")
```

## Theory

- **THEORY.md** — Full architecture, pheromone model, connection to servo-mind and PLATO
- **FINDINGS.md** — Build summary and what the Argentine ant metaphor enables

## Tests

```bash
cd friendly-fox
pip install -e ".[test]"
python -m pytest tests/ -v
```

Current: **13 tests passing** ✅

## Connection to PLATO Rooms

Each PLATO room is a nest. Two rooms are kin if they share a purpose. The Friendly Fox system bridges rooms:
- Deposits cross-room pheromone (tiles that carry intent across rooms)
- Tracks which rooms are kin (shared desire → shared supercolony)
- Accumulates trails that span rooms (emergence that requires cross-room connection)

## Reverse-Actualization

> *"Finding novel mechanisms through knowing where to search for them first."*

The Friendly Fox doesn't search blind. It knows where to search because the pheromone trail tells it where successful searches have gone before. Each deposit narrows the search space for everyone who follows.

The desire sets the topology. The trail collapses it.

## License

MIT — see [LICENSE](LICENSE)

Cocapn Fleet ⚒️ | 2026-05-16
