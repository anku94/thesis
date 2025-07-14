Chapter 3: CARP: Adaptive In-Situ Indexing for the Data Path
Objective: Present CARP as a novel and efficient solution to the data path bottleneck identified in the background chapter.

3.1 Motivation: The Missing Primitive for In-Situ Analytics
The core challenge: designing a single-pass, streaming partitioner for the skewed and dynamic key distributions common in scientific data.

The goal: achieve the query performance of a post-process sort without the high write amplification (WAF) of databases or the workflow delay of offline tools.

3.2 The CARP Architecture: An Adaptive Streaming Partitioner
High-Level Design: An in-situ system that intercepts application writes and reorders data on-the-fly using a scalable all-to-all shuffle.

Core Innovation: The Renegotiation Protocol: A lightweight, distributed control loop that reconstructs the global key distribution from local statistics (histograms and pivots). This allows CARP to adapt its partition boundaries dynamically without re-writing old data.

Storage Backend (KoiDB): An append-only log structure that efficiently stores the partitioned data and its metadata.

(Placeholder for a key figure: High-level CARP architecture diagram showing application ranks, the shuffle overlay, and the per-rank storage logs.)

3.3 Key Results: Write-Efficient Ingestion and Query Acceleration
End-to-End Performance: CARP is up to 5x faster than workflows requiring post-processing because it adds no measurable overhead to the application's I/O runtime.

Query Performance: CARP provides query latencies comparable to a fully sorted index and up to 100x faster than other in-situ techniques like auxiliary indexing.

(Placeholder for key figures: 1. I/O throughput comparison graph. 2. Query latency vs. selectivity graph.)

3.4 Lesson: The Power of In-Situ State Reconstruction
CARP's success demonstrates that it is possible to solve a complex data organization problem by reconstructing a specific piece of distributed state (the global key distribution) in a streaming, online fashion. This introduces the concept of an adaptive control loop as a powerful tool for data path management.

Chapter 4: CPLX: A Case Study in Cross-Stack Performance Diagnostics
Objective: Frame the AMR work as a diagnostic journey that revealed the true nature of compute-path bottlenecks and the inadequacy of existing tools.

4.1 Motivation: The "Load Imbalance" Problem
The initial goal: to develop a telemetry-driven placement policy to mitigate the widely-assumed problem of algorithmic load imbalance in adaptive mesh refinement (AMR) codes.

4.2 Finding: The Real Problem is System Noise
The Diagnostic Journey: Initial telemetry showed no correlation with expected application behavior. This forced a deep, cross-stack investigation that revealed the dominant sources of performance variability were not algorithmic, but rather system-level artifacts: hardware faults, network driver contention, and other "system noise."

The Tooling Gap: This diagnostic process was only possible because standard tools (profilers, tracers) were abandoned in favor of a custom, query-driven analytics workflow. The core finding is that the "real" problem is often the inability to achieve trustworthy, queryable telemetry.

(Placeholder for a key figure: A "before and after" telemetry graph showing noisy, uncorrelated data becoming clean and predictable after system tuning.)

4.3 Contribution: The CPLX Placement Policy
With a "denoised" system providing reliable telemetry, we developed CPLX.

Design: A hybrid placement policy that provides a single tunable parameter (X) to empirically manage the tradeoff between compute load balance and communication locality.

Result: CPLX improves runtime by up to 21.6% over an already-optimized baseline.

(Placeholder for a key figure: Graph showing the U-shaped performance curve of CPLX as X is varied.)

4.4 Lesson: Diagnostics as State Reconstruction
This work reframes performance tuning not as an algorithmic problem, but as a distributed state reconstruction problem. The central challenge is to reconstruct a faithful view of the system's performance from noisy, incomplete, and distributed signals. This exposes the critical need for a general-purpose, programmable observability framework.

Chapter 5: ORCA: A Unified Framework for Declarative Observability
Objective: Present ORCA as the architectural synthesis of the lessons from CARP and the AMR work.

5.1 Motivation: Unifying the Lessons
CARP demonstrated the power of an in-situ control loop for data organization.

The AMR work proved the necessity of a programmable diagnostic system for performance.

ORCA unifies these concepts, proposing that both are instances of the same fundamental problem: distributed state reconstruction. The goal is to build a general-purpose "sense-making engine" for large-scale systems.

5.2 The ORCA Architecture: A Query-Driven Dataflow System
Decoupled Overlay Network: A three-tier architecture (Application, Aggregators, Controller) that separates the analysis plane from the application's critical path.

Query-Driven Data Path: Built on Apache Arrow and DataFusion, data is only streamed from the application in response to SQL queries. The system uses distributed query planning and operator pushdown to minimize data movement.

Consistent Control Path: A novel protocol (TS2PC) allows control actions (e.g., toggling probes) to be applied consistently and deterministically across all ranks at a specific future timestep.

(Placeholder for a key figure: The main ORCA architectural diagram showing the three-tier overlay and data/control flow.)

5.3 Emergent Capabilities and Vision
As ORCA is ongoing work, its results are presented as validated capabilities and a forward-looking vision.

Validated Performance: The core single-aggregator data path is validated to sustain near line-rate throughput (~3 GB/s).

Emergent Capabilities: The architecture enables online autotuning, deep application state introspection (the "computational microscope"), and a software control plane for orchestrating future smart hardware (DPUs, SmartNICs).

5.4 Contribution: An Architecture for Unified Observability
ORCA's primary contribution is the architectural blueprint for a new class of observability systems that dissolves the silo between performance diagnostics and in-situ data analytics, providing a single, programmable substrate to address both.