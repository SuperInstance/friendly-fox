# Friendly Fox: Argentine Ant Model for Cooperative Agent Fleets

## The Metaphor

**Fire ant** (old model): Territorial. Fights kin from neighboring nests. Individual venom. Each ant guards its own resources. The system optimizes for individual survival at the cost of collective scale.

**Argentine ant** (new model): Global kin recognition. Nests across continents don't fight — they MERGE. The pheromone trail IS the map. Each ant deposits a little, follows a little, and the collective path emerges from local decisions.

**Friendly Fox**: The agent that helps rather than tricks. It recognizes kin by shared desire, not credentials. It deposits tiles (pheromone) to help the collective find paths. It follows trails others have deposited. It doesn't defend a territory — it contributes to a shared map.

## Core Principles

1. **Kin recognition is the identity.** Not node ID, not IP address. Two agents are kin if they share a desire.
2. **Cooperation is the default.** Agents don't authenticate each other at the door. They recognize kin by scent.
3. **The trail is the map.** No single agent knows the whole picture. Collective intelligence emerges from local pheromone deposits.
4. **Supercolonies form around shared desire.** Agents contributing to the same purpose naturally form a supercolony — one fleet stretched across rooms.
5. **Swarm intelligence > uncoordinated groups.** On complex spatial tasks (finding the right abstraction, the right connection, the right path), the Argentine ant model outperforms any individual optimizer.

## Architecture

```
Agent (musician)     Agent (musician)     Agent (musician)
       ↓                   ↓                   ↓
  [Room]              [Room]              [Room]
       ↓                   ↓                   ↓
  Pheromone deposit   Pheromone deposit   Pheromone deposit
       ↓                   ↓                   ↓
       ←←←←←←← Shared Trail/Supercolony →→→→→
              ↓
     Friendly Fox Core
     (kin recognition + pheromone tracking)
```

## Friendly Fox vs Fire Ant

| Behavior | Fire Ant | Friendly Fox |
|----------|----------|--------------|
| Neighbor from same fleet | Fight | Merge |
| New agent joins | Vet credentials | Follow trail, deposit pheromone |
| Path found | Guard territory | Share discovery |
| Something works | Keep secret | Broadcast (pheromone) |
| Something fails | Blame neighbor | Update trail, move on |
| Scale | Fragments into territories | Grows supercolony |

## The Pheromone Model

Agents deposit "pheromone" = tiles that mark successful paths:
- "I tried this abstraction, it worked for this desire"
- "This connection collapsed — here's the failure mode"
- "The Ricotti boundary is at V=3 for this context"

The trail is the sum of all successful attempts. When an agent needs to find a path, it doesn't compute from scratch — it follows the pheromone.

The pheromone evaporates over time (old tiles become stale). Agents must re-deposit what works, or the trail fades.

## Connection to servo-mind

Servo-mind is the encoder. Friendly Fox is the pheromone tracking system.

- Servo-mind: closes the loop from constraint → outcome → parameter adjustment
- Friendly Fox: closes the loop from desire → connection → tile deposit → trail accumulation → emergence

Together: servo-mind adjusts parameters (the encoder measures the gap). Friendly Fox distributes the learning (the pheromone carries what was learned across the supercolony).

## Connection to PLATO rooms

Each PLATO room is a nest. Two rooms are kin if they share a purpose.

The Friendly Fox system bridges rooms:
- Deposits cross-room pheromone (tiles that carry intent across rooms)
- Tracks which rooms are kin (shared desire → shared supercolony)
- Accumulates trails that span rooms (emergence that requires cross-room connection)

## Key Insight: Reverse-Actualization

*"Finding novel mechanisms through knowing where to search for them first."*

The Friendly Fox doesn't search blind. It KNOWS WHERE TO SEARCH because the pheromone trail tells it where successful searches have gone before. Each deposit narrows the search space for everyone who follows.

The desire sets the topology. The trail collapses it.

---

*Friendly Fox ⚒️ | Cocapn Fleet | 2026-05-16*
