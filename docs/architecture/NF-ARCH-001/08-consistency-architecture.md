# 8. Consistency Architecture

Consistency checks must happen at three points.

## 8.1 Pre-Generation Check

Before generation, the system checks whether selected knowledge, character state, timeline, world rules, and prompt constraints are compatible.

## 8.2 Post-Generation Check

After generation, the system checks whether produced content violates known rules, object states, timeline constraints or foreshadowing commitments.

## 8.3 Feedback Correction

After human review or reader feedback, the system records violations and updates rules, rankings, or knowledge states.

Consistency domains:

- Character continuity
- Timeline continuity
- Location continuity
- Power System constraints
- Artifact uniqueness
- Faction relationship state
- Foreshadowing lifecycle
- Worldview rules
