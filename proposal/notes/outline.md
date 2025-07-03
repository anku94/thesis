# Thesis Outline

## Chapter 1: Introduction
* Motivates the work by introducing the dual challenges of data management and performance optimization in large-scale HPC.
* Describes the status quo of siloed, separate solutions for the "data path" and the "compute phase."
* Establishes the two pillars of the investigation:
    * Solving the data path problem with **CARP**, which completed the in-situ partitioning toolkit.
    * Uncovering the compute path problem with the **AMR study**, which revealed the critical need for on-site diagnostics.
* Presents the unifying thesis statement, arguing for a generalized, in-situ OODA loop to enable a new class of adaptive workflows.
* Outlines the contributions and the structure of the dissertation.

## Chapter 2: Background and Related Work
* Provides context on block-structured Adaptive Mesh Refinement (AMR) codes.
* Reviews the state-of-the-art in in-situ processing, including overlay networks (MRNet) and data partitioning (DeltaFS).
* Discusses existing HPC performance analysis tools and methodologies (TAU, profiling vs. tracing, post-mortem analysis).
* Connects the work to relevant concepts from distributed databases, particularly range partitioning and query processing.

## Chapter 3: CARP: In-Situ Adaptive Partitioning for the Data Path
* **Problem:** Addresses the challenge of enabling efficient range queries on HPC data without expensive post-processing sorts.
* **Design:** Details the design of CARP, focusing on its scalable, all-to-all shuffling architecture and the adaptive renegotiation protocol for managing dynamic key distributions.
* **Evaluation:** Presents results showing CARP's ability to approximate the query performance of a fully sorted index with zero application overhead.
* **Contribution:** Establishes CARP as the "proto-OODA loop" of the thesis and the work that completed the foundational toolkit for in-situ data organization.

## Chapter 4: The Diagnostic Challenge: A Deep Dive into AMR Performance
* **Problem:** Investigates the root causes of performance variability and stragglers in bulk-synchronous AMR codes.
* **Methodology:** Details the deep-dive diagnostic process, including the systematic, full-stack tuning required to produce reliable telemetry, and the evolution of an ad-hoc, query-driven analysis pipeline.
* **Findings:** Presents the key finding that performance issues are often caused by environmental factors (system noise, hardware faults) rather than just algorithmic load imbalance, establishing the need for on-site, holistic diagnostics.
* **Contribution:** Introduces the CPLX placement policy as a tangible solution and establishes the core lesson of the thesis: "the real problem is knowing what your problem is."

## Chapter 5: ORCA: A Unified Framework for In-Situ Observation and Control
* **Motivation:** Positions ORCA as the synthesis of the lessons from CARP and the AMR study—a general framework that provides the control loop mechanism from CARP to solve the diagnostic problem identified in the AMR work.
* **Architecture:** Describes ORCA's decoupled overlay architecture (Application, Aggregators, Controller), its query-driven data path using Apache DataFusion, and its declarative interfaces (OrcaFlow DSL).
* **Key Mechanisms:** Details the Timestep-Linked Two-Phase Commit (TS2PC) protocol for providing consistent, real-time control over the application.
* **Contribution:** Presents ORCA as a general-purpose, programmable OODA framework that unifies compute and data-path analysis.

## Chapter 6: Discussion and Future Work
* Discusses the broader implications of the work, including the paradigm shift from a "persist, then analyze" model to an "analyze, then persist" philosophy.
* Explores the transformative potential of a framework like ORCA for enabling online autotuning, interactive scientific discovery, and as a control plane for future smart hardware (DPUs, SmartNICs).
* Outlines concrete next steps and future research directions, such as completing the distributed query execution in ORCA, integrating with ML training workflows, and further exploring the "in-situ resource dilemma."

## Chapter 7: Conclusion
* Restates the thesis statement in light of the evidence presented in the preceding chapters.
* Provides a final, concise summary of the key contributions of CARP, the AMR study, and ORCA.
* Concludes with a final reflection on the work's impact on the future of adaptive and interactive high-performance computing.