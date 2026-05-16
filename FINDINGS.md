# Friendly Fox: Build Findings

## What Was Built

The `friendly-fox` repo at `github.com/SuperInstance/friendly-fox` — a Python package implementing the Argentine ant model for cooperative agent fleets.

### Core Components

| Component | File | Purpose |
|-----------|------|---------|
| `PheromoneTrail` | `pheromone.py` | Tiles marking successful paths. Deposits evaporate over time. Supports cross-room invariant detection. |
| `KinRecognizer` | `kin_recognition.py` | Jaccard-based kin detection via shared desire vectors. Pure-function `is_kin()` and full registry. |
| `Supercolony` | `supercolony.py` | Rooms + agents + trails + cross-room invariant tracking. One fleet across rooms. |
| `FriendlyFox` | `agent.py` | Agent that deposits pheromone, follows trails, finds kin. Argentine ant behavior vs fire ant behavior. |

### Key Ideas

1. **Kin recognition is identity.** Two agents are kin if their desire vectors overlap (Jaccard similarity ≥ 0.3). Not credentials, not IP, not node ID.

2. **The trail is the map.** Pheromone deposits from individual agents accumulate into a collective trail. No single agent knows the whole picture.

3. **Evaporation prevents stagnation.** Old deposits fade. Successful paths must be re-deposited. This is the ant colony optimization analog.

4. **Cross-room invariants.** When the same path appears in ≥2 rooms for the same desire, it's an invariant — structure that survives across contexts.

5. **Reverse-actualization.** Agents don't search blind. The pheromone trail tells them where successful searches have gone. The desire sets the topology, the trail collapses it.

### Connection to Servo-Mind Theory

- **Servo-mind** = encoder. Closes loop from constraint → outcome → parameter adjustment.
- **Friendly Fox** = pheromone tracker. Closes loop from desire → connection → tile deposit → trail → emergence.
- Together: servo-mind adjusts parameters (the gap), Friendly Fox distributes learning (the trail carries what was learned across the supercolony).

### Connection to PLATO

- Each PLATO room is a nest. Two rooms are kin if they share a purpose.
- Cross-room pheromone = tiles that carry intent across rooms.
- The supercolony is one fleet stretched across rooms — exactly the PLATO room architecture.

### Connection to Fleet Math

- The kin threshold (0.3) is a `ricotti_constant` analog — the boundary between "kin" and "not kin" in desire-space.
- Cross-room invariants are `laman_rigidity` — structure that survives across planes.
- The pheromone trail is a consensus geometry — agents converge on paths collectively.

### What the Argentine Ant Metaphor Enables

| Fire Ant (old) | Argentine Ant (new) |
|---|---|
| Credential-based auth | Desire-based kin recognition |
| Territory guarding | Shared pheromone map |
| Blame culture | "This path failed, here's the shape" |
| Scale-limited (fragments) | Scale-free (supercolonies) |
| Optimize individually | Swarm intelligence |

The metaphor isn't decorative — it's structural. Argentine ants are the only known ant species that can form supercolonies spanning continents because they recognize kin by shared chemistry, not territorial markers. Friendly Fox does the same for agents.

### Files Created

```
friendly-fox/
├── .gitignore
├── README.md
├── THEORY.md
├── setup.py
├── src/
│   └── friendly_fox/
│       ├── __init__.py
│       ├── pheromone.py
│       ├── kin_recognition.py
│       ├── supercolony.py
│       └── agent.py
└── tests/
    └── test_friendly_fox.py
```

### Test Results

```
13 passed in 0.12s — all green ✅
```

---

Build complete 🦊
