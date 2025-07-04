# AMR — Diagnosing and Optimizing Adaptive Mesh Codes

## Background and Motivation

  * Block-structured AMR (Adaptive Mesh Refinement) codes are widely used for large-scale simulations in physics and engineering, but are notoriously difficult to optimize at scale.
  * Synchronization and frequent mesh refinement create straggler effects; performance is traditionally diagnosed as a load-balancing problem.

## Load-Balancing Policies and Baselines

  * Common practice: work placement policies (e.g., Space-Filling Curves, naive block distribution) assume uniform costs and static assignment.
  * Prior literature and production codes rely on heuristics; empirical tuning is difficult, and “obvious” improvements often fail at scale.

## The Diagnostic Journey

  * Initial attempts to optimize placement exposed more complex bottlenecks: hardware faults, system noise, and non-obvious sources of variability.
  * Standard profiling tools were insufficient—transient effects and cross-stack anomalies went undetected.

## Evolution of the Telemetry Pipeline

  * Necessity drove a bottom-up diagnostic process: custom code instrumentation, direct CSV logging, and iterative data analysis.
  * The ad-hoc telemetry stack evolved into a query-driven, structured workflow, borrowing concepts from modern OLAP and observability.
  * Adoption of programmable tools (eBPF, OLAP engines) enabled the root-cause diagnosis that classical HPC tools could not deliver.

## Key Results and Policy Development

  * The CPLX placement policy: a tunable hybrid balancing load and communication locality, outperforming prior baselines by up to 21.6%.
  * Main finding: true bottlenecks often lie outside what classical load balancing or placement can solve—highlighting the need for deeper, programmable, telemetry-driven diagnosis.

## Broader Lessons

  * Performance optimization for modern AMR codes is fundamentally empirical and diagnostic, not purely algorithmic.
  * Motivates the need for a general, programmable approach to cluster telemetry and control—setting the stage for ORCA.
