# Complete Thesis Document Outline

## Chapter 1: Introduction

* Motivation: Data organization and performance variability as central challenges in modern cluster-scale computing (HPC and ML).
* Existing silos: Why data and compute have traditionally been addressed separately—and why that is breaking down.
* Brief orientation: Bulk Synchronous Parallel (BSP) as the unifying abstraction.
* Thesis statement: Streaming, programmable analytics and control can unify and address both data and compute challenges.
* Contributions overview: CARP (in-situ data), CPLX/AMR (empirical tuning), ORCA (unified framework).

## Chapter 2: Background and Landscape

* BSP paradigm in depth: synchronization, phases, and why it models both HPC and ML at scale.
* Cluster anatomy: compute, memory, network fabrics (HPC: collectives/control; ML: backend/frontend), parallel filesystems.
* Data movement and storage: bursty checkpointing, the network/storage bandwidth mismatch, implications for workflow design.
* Job lifecycles: long-lived runs, resilience needs, and checkpointing roles (analysis in science, recoverability in ML).
* The rise of in-situ analytics: why “dump and analyze later” is failing; data reduction and analysis at the source as a pressing community concern.
* The scientific code ecosystem:
  * How open-source, institutional, and domain-driven codes shape the landscape.
  * VPIC: particle-in-cell, plasma/astro applications, I/O stress.
  * AMR codes: Parthenon, FLASH, Enzo; multiscale adaptivity in science.
  * Context for the broader world: These codes exemplify—but do not exhaust—the range of modern scientific applications.

## Chapter 3: CARP—In-Situ Range Partitioning

* The missing piece in practical in-situ analytics: range partitioning for efficient queries on streaming scientific data.
* Limitations of traditional post-processing and previous in-situ approaches.
* CARP system design: adaptive, online range partitioning during I/O; robustness to skew and changing distributions.
* Implementation and validation: performance, scalability, and impact on time-to-analysis.
* CARP as an early instance of a system-state-driven, in-situ control loop.

## Chapter 4: Diagnosing Variability in AMR Codes

* The challenge of stragglers and unpredictable performance in adaptive parallel codes.
* Why standard profiling tools fail at scale; emergence of telemetry-driven, empirical workflows.
* CPLX: a tunable placement policy that balances compute load and locality, informed by fine-grained diagnostics.
* Empirical findings: hardware/environmental variability often dominates algorithmic load imbalance.
* Broader takeaway: Optimization starts with diagnosing the real, often hidden, sources of variability.

## Chapter 5: ORCA—Unifying Observability and Control

* Motivation: From in-situ analytics to unified, real-time, programmable observability and control.
* ORCA architecture: overlay network, distributed queries (Apache DataFusion), decoupled data and control paths.
* Integrating lessons from CARP and AMR: data-driven control loops, empirical diagnostics, programmability.
* Consistent, cluster-wide steering (TS2PC protocol) for robust runtime tuning.
* Toward a declarative, extensible framework for analysis and control at scale.
