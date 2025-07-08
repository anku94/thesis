## Motivation: Efficiency challenges on both data and compute paths

"GA: Write with a focus on opportunities: e.g. due to inefficiencies"

## Status Quo and Efficiency Bottlenecks

In-situ reorganization toolkit incomplete. Forced between bad options.

Compute path: nominally load balancing, but no characterization. No agreement on distributions, frequencies etc.

## Our Work: From Specific Solutions to a General-Purpose Framework

This work first addresses critical efficiency bottlenecks on the data and compute paths separately. These efforts filled critical gaps in understanding and solving these efficiency bottlenecks, but also produced lessons and revealed the factors that limited their accessibility. Building on these lessons, we then produce a general-purpose framework.

### Data Path: Streaming Data Reorganization

Motivation: a write-optimized ingestion system for range queries.

Challenges: scale, dynamism, skew, etc.

Our Contribution: CARP, an in-situ partitioner.

Lessons learned: analytics capabilities are fragmented. Databases are able to leverage multiple index types by decoupling analyses from data layouts.

### Compute Path: Addressing "Computational Load Imbalance"

Motivation: imbalance widely documented. let's use telemetry to craft placement policies.

Challenges:

1. Telemetry did not make sense. Had to do deep dives
2. Tools unhelpful. Had to develop own pipeline.
3. Placement policy algorithm challenge + tuning challenge.

Our Contribution: CPLX, a placement policy. 20\% improvement over optimized baselines.

Lessons learned:

1. "Load imbalance" is a misnomer. Variability a problem.
2. No universal solutions. Context-specific. Knowing context is key. Can't export traces.
3. Organically developed telemetry pipeline demonstrated the need for analytical telemetry over traces.

### Unifying Observability, Analytics, and Online Control

Motivation: need on-situ, in-situ, programmable observability

Challenges: completely new capability/system. No template. Complex and involves a lot of moving parts.

Our Contribution: ORCA, a general-purpose framework.

## Thesis Statement and Potential Impact

Thesis statement: you can do whatever with in-situ. It is all needed. Combine with Arrow and SQL to get reusability, modularity, composability etc. One approach works for everything.

Expected changes to the SoTA after this work: immediate transformation in the way we do performance. "profiling to tracing" becomes a common-case real-time spectrum nagivated as the application executes.

Over time, the "universal langauge" nature of Arrow/SQL will enable it to subsume more workflows. Richer operator types, more extensive query types, more data sources/drivers, accelerator support etc. This is the framework that brings all these capabilities within the reach of a common umbrella.

## Document Structure
