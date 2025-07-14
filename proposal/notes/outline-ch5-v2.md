Chapter X: ORCA: A Unified Framework for Declarative Observability
1. Motivation: Principles for an Ideal Observability System

The central motivation for ORCA is to realize a new vision for distributed observability: what if a monitoring system could function as a query engine for an entire cluster? A user should be able to ask a complex question about the system's state, and the framework should orchestrate the necessary data movement and computation to provide a real-time answer.

Our prior work on the data path (CARP) and compute path (AMR/CPLX) revealed that such a system must be built on three core principles:

Programmability: The user must be able to define what data sources to tap, what schemas to expose, and how to aggregate the resulting telemetry. Our work showed that fixed-schema tools are insufficient for the dynamic and idiosyncratic nature of performance bottlenecks.

Real-Time, Coordinated Analytics: Insights must be produced as the application runs, with minimal delay. Crucially, the system must preserve the structured nature of BSP execution—especially timestep alignment—to make telemetry interpretable and enable meaningful, coordinated views across ranks.

Interactivity: Effective observability requires a full spectrum of workflows, from low-overhead monitoring to detailed root-cause localization. This necessitates the ability to dynamically insert probes, reconfigure aggregations, and adapt queries mid-execution, all while maintaining consistency with application progress.

2. Background: The Observability Gap in BSP Systems

While numerous observability tools exist, they were not designed to meet the specific, coordinated needs of large-scale BSP applications. As illustrated in Figure X.X, traditional approaches fall short of the principles outlined above. Tracing often captures excessive data, making real-time analysis infeasible. Profiling loses critical temporal detail by collapsing data into summaries, and sampling provides an uncoordinated, statistically incomplete picture that breaks the spatial and temporal structure of the problem.

It is also important to distinguish ORCA's role from that of a Time Series Database (TSDB). ORCA is not a storage system; it is a complementary, in-memory pre-processing frontend. Its purpose is to perform low-intrusion data collection, use intelligent query planning to filter and aggregate data as close to the source as possible, and then route the processed results to various sinks. These sinks can include a TSDB for long-term storage, Parquet files for offline analysis, or a live visualization tool. ORCA's primary function is to intelligently decide what data is worth persisting in the first place.

3. The ORCA Architecture: A Declarative Dataflow Engine

ORCA is architected as a sense-making engine that materializes on-demand views of a distributed system, operating on an analyze, then persist philosophy. Its design rests on three architectural pillars. First, a decoupled overlay network of a controller and aggregators separates the analysis plane from the application's critical path. Second, a query-driven data path uses Apache Arrow and Datafusion to stream and process telemetry only in response to SQL queries, with optimizations like operator pushdown to minimize data movement. Third, a consistent control path, using the Timestep-Linked Two-Phase Commit (TS2PC) protocol, enables control actions like toggling probes to be applied deterministically across all ranks at a specific application timestep.

4. Capabilities and Impact

ORCA's architecture provides a powerful substrate with immediate and broad-ranging impact for any BSP workload, including both HPC simulations and ML training.

Full-Spectrum, Real-Time Diagnostics: ORCA integrates metrics, tracing, and profiling into a single, queryable continuum. It directly addresses the diagnostic challenges from the AMR work by enabling developers to dynamically insert probes, correlate events across the cluster, and perform root-cause analysis in real-time.

A General-Purpose Substrate to Inform and Enforce: The framework is a general engine for materializing distributed state. This allows it to inform other specialized tools by performing in-situ data reduction and feeding curated data streams to visualization engines like ParaView/VisIt. It can also enforce correctness policies, such as detecting silent data corruptions in ML training, by defining the required state via SQL and UDFs.

5. Future Vision: Towards a Unified Analytics Plane

The long-term vision for ORCA is to serve as a single, programmable fabric for the entire in-situ ecosystem. Its architecture, built on Datafusion, provides a practical path for implementing Science SQL concepts, extending its query capabilities to non-relational scientific data like unstructured meshes. Its declarative dataflow model also positions it as an ideal software control plane for orchestrating smart infrastructure, pushing analysis down to DPUs or SmartNICs. Ultimately, ORCA aims to unify data analytics, performance diagnostics, and adaptive control within one coherent framework.