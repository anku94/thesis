# Chapter 1: Introduction - Complete Outline

## Motivation: Efficiency at Datacenter Scale

BSP applications power critical computational infrastructure - large-scale scientific simulations, distributed ML training, climate modeling, astrophysics codes. These workloads operate at tens of thousands of accelerator nodes and continue to grow.

Scale creates datacenter-level efficiency impacts:
- Cost: Inefficiencies multiply across thousands of nodes
- Time-to-discovery: Performance bottlenecks delay scientific progress
- Resource utilization: Idle cycles represent massive waste

Two primary efficiency challenges:
- **Data path**: Bursts of checkpointed state create I/O bottlenecks
- **Compute path**: Global synchronization amplifies sensitivity to execution variability

## Status Quo and Efficiency Bottlenecks

### Data Path: Incomplete In-Situ Toolkit

Current approaches force poor trade-offs:
- **Post-processing sorts**: Optimal query performance but expensive, slow analysis pipeline
- **Auxiliary indices**: Avoid reordering but poor query performance due to random access
- **Hash partitioning**: Excellent for point queries but destroys ordering for range queries
- **Missing primitive**: Adaptive range partitioning for dynamic, skewed distributions

Scientific data characteristics make static solutions inadequate:
- Highly skewed distributions (particle energies, temperatures)
- Dynamic evolution of distributions over time
- Need for efficient range queries on continuous attributes

### Compute Path: Poor Performance Characterization

"Load imbalance" widely acknowledged but poorly understood:
- No systematic studies of distributions, frequencies, or root causes
- Coarse-grained tools provide misleading aggregates
- Fine-grained tools generate unusable trace volumes
- Ad-hoc solutions used by scientists without principled methodology

Cross-stack complexity makes diagnosis difficult:
- Hardware thermal throttling
- Driver stalls and network contention
- OS-level interruptions
- Interactions between application, MPI, and system layers

## Our Work: From Specific Solutions to a General-Purpose Framework

This work addresses critical efficiency bottlenecks on data and compute paths separately, revealing fundamental limitations in current approaches and culminating in a unified framework.

### Data Path: CARP - Adaptive Range Partitioning

**Motivation**: Enable efficient range queries on streaming scientific data without expensive post-processing.

**Challenges**:
- Scale: Must work at tens of thousands of cores
- Dynamism: Distributions evolve during simulation
- Skew: Highly non-uniform data distributions
- Overhead: Cannot impact application performance

**Our Contribution**: CARP - Continuous, Adaptive Range Partitioner
- In-situ adaptive repartitioning based on observed key distributions
- Scalable renegotiation protocol using distributed histograms
- Approximates perfectly sorted performance with no ingestion overhead
- 5x faster end-to-end than post-processing, 100x faster queries than auxiliary indices

**Lessons Learned**:
- Analytics capabilities are fragmented across specialized tools
- Database-style modularity needed - decouple analysis from data layout
- Adaptive control loops essential for dynamic workloads
- In-situ processing enables "good enough" solutions that outperform "perfect" offline approaches

### Compute Path: Untangling "Load Imbalance"

**Motivation**: Use fine-grained telemetry to develop placement policies for AMR codes suffering from straggler problems.

**Challenges**:
1. **Telemetry reliability**: Raw measurements didn't correlate with expected behavior
2. **Tooling limitations**: Standard profilers/tracers inadequate for root-cause analysis
3. **Cross-stack complexity**: Multiple interacting sources of variability
4. **Algorithmic design**: Balancing load vs. communication locality

**Our Contribution**: CPLX placement policy + diagnostic methodology
- Systematic approach to establishing "clean room" measurement environment
- Custom telemetry pipeline using structured analytics (ClickHouse, SQL)
- Tunable placement policy managing load balance vs. locality trade-off
- 21.6% runtime improvement over optimized baselines

**Lessons Learned**:
1. "Load imbalance" is misnomer - real problem is cross-stack variability
2. Context-specific solutions required - can't export traces and maintain insight
3. Programmable telemetry essential - ad-hoc analytics pipeline more effective than standard tools
4. Real-time feedback needed for effective diagnosis and tuning

### Unifying Framework: ORCA - Programmable Streaming Analytics

**Motivation**: Generalize lessons from data and compute path work into accessible, programmable observability framework.

**Challenges**:
- No existing template for cluster-scale streaming analytics
- Complex distributed system with multiple interacting components
- Performance requirements - must not impact application critical path
- Generality vs. efficiency trade-offs

**Our Contribution**: ORCA - Observability with Realtime Control and Aggregation
- Query-driven data collection using Apache Arrow and DataFusion
- Declarative analysis pipelines with real-time control capabilities
- "Analyze then persist" philosophy - only store results, not raw data
- Scalable overlay architecture decoupled from application

**Unifying Insight**: Both data and compute path challenges require same primitive - programmable, real-time streaming analytics for actionable system insight.

## Thesis Statement and Potential Impact

**Thesis**: By treating both scientific data and performance telemetry as queryable streams within a unified, programmable dataflow framework, the distinct challenges of data management and compute-path optimization in large-scale synchronous applications can be solved with a single, general-purpose methodology.

**Technical Approach**: Unified streaming analytics framework using Apache Arrow/SQL provides reusable, modular, and composable approach to in-situ workflows.

**Short-term Impact**: Immediate transformation in performance tooling - "profiling to tracing" becomes real-time spectrum navigated during application execution.

**Long-term Impact**: Universal language for in-situ workflows enables subsumption of diverse analytics through extensible operator types, query capabilities, and data sources.

## Contributions and Document Structure

### Three Major Contributions

1. **CARP**: Fills critical gap in in-situ data organization with first scalable system for adaptive range partitioning, completing toolkit of fundamental partitioning primitives.

2. **AMR Performance Study**: Develops programmable, empirical workflows for real-world performance diagnosis, demonstrating necessity of query-driven telemetry and revealing that core problem is understanding the problem itself.

3. **ORCA**: Generalizes insights into unified, real-time observability framework providing programmable substrate for both data analytics and system optimization.

### Document Structure

- **Chapter 1**: Introduction and motivation
- **Chapter 2**: Background on BSP systems, in-situ computing, and observability
- **Chapter 3**: CARP - Adaptive range partitioning for streaming scientific data
- **Chapter 4**: AMR performance study - Systematic approach to variability diagnosis
- **Chapter 5**: ORCA - Unified framework for streaming analytics and control
- **Chapter 6**: Conclusions and future work

Each technical chapter follows consistent structure: motivation, related work, system design, evaluation, lessons learned.
