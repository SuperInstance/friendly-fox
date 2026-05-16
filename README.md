# friendly-fox ⚒️🦊

**Argentine ant model for cooperative agent fleets.**

The agent that helps rather than tricks. No credentials. No territory. Just shared desire and shared trails.

## Quick Start

```python
from friendly_fox import Supercolony, FriendlyFox

# Create a supercolony (one fleet stretched across rooms)
colony = Supercolony("fishing_fleet")
colony.add_room("mediterranean", purpose="find fish")

# Agents join by shared desire, not credentials
fox_1 = FriendlyFox("boat_1", ["fish_better", "save_fuel"], "mediterranean")
fox_1.join_supercolony(colony)

fox_2 = FriendlyFox("boat_2", ["fish_better", "map_depth"], "mediterranean")
fox_2.join_supercolony(colony)

# Deposit pheromone — mark a successful path
fox_1.deposit_success("fish_better", "follow_sounder_pattern_near_rock")

# Follow the trail — don't search blind
trail = fox_2.follow_trail("fish_better")
print(f"Found {len(trail)} paths from kin")
```

## Core Concept

```
Fire Ant (old):        Friendly Fox (new):
- Territorial          - Argentine ant kin recognition
- Fights kin           - Merges with kin across continents
- Guards resources     - Deposits pheromone for all
- Individual optimize  - Swarm intelligence
```

**Friendly Fox agents are Argentine ants.** They recognize kin by shared desire, not credentials. They deposit pheromone (tiles) to mark successful paths for everyone. They follow existing trails before searching blind.

## Docs

- [THEORY.md](THEORY.md) — Full theory and architecture
- [docs/](docs/) — Additional documentation

## Install

```bash
pip install friendly-fox
```

Or from source:
```bash
git clone https://github.com/SuperInstance/friendly-fox
cd friendly-fox
pip install -e .
```

## Tests

```bash
python3 tests/test_friendly_fox.py
```

## License

MIT | Cocapn Fleet | 2026-05-16
