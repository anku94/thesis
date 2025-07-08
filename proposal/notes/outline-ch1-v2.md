### **Chapter 1: Introduction**

#### **Motivation and Scope**

The Bulk Synchronous Parallel (BSP) paradigm powers some of our most critical computational tools, from large-scale scientific simulations in astrophysics and climate science to distributed training of foundation models in machine learning. These workloads—consisting of large parallel computations interspersed with I/O and global synchronization—currently operate at the scale of tens of thousands of accelerator nodes and continue to grow. As these applications scale, their efficiency has datacenter-level impacts on both cost and time-to-discovery.

The tightly synchronized nature of BSP creates two unique challenges that strain modern computing infrastructure. On the **data path**, bursts of checkpointed state create massive I/O demands on the storage and analytics infrastructure. On the **compute path**, frequent global synchronization amplifies the system's sensitivity to execution variability. Performance bottlenecks that would be manageable in loosely coupled systems, such as minor OS-level interruptions or thermal throttling, become critical scaling barriers when every worker must wait for the slowest participant in a phenomenon known as the **straggler problem**. Prior work has shown this MPI waiting time can exceed 60% of the total runtime at scale, making these inefficiencies a primary obstacle to progress.

#### **Status Quo: A Siloed In-Situ Landscape**

In response to these challenges, the high-performance computing community developed the "in-situ" paradigm, aiming to process data while it is still resident in memory to reduce I/O and accelerate analysis. However, the landscape of tools that emerged was largely siloed, with separate solutions evolving to address the distinct data and compute path challenges.

To address the **data path challenge**, a rich ecosystem of tools was developed for in-situ data reduction and management.
* **Visualization-centric frameworks** like ParaView/Catalyst and VisIt/LibSim focused on embedding rendering engines directly into simulations to generate images on the fly.
* **Data management systems** like ADIOS provided flexible middleware to adapt I/O patterns, while systems like DataSpaces offered shared-memory abstractions.
* The state-of-the-art in in-situ *data organization* was **DeltaFS**, which demonstrated scalable hash partitioning of data as it streamed to storage. This was highly effective for point queries but, by design, destroyed key locality, making it unsuitable for range queries. Adaptive range partitioning—a critical primitive for scientific discovery—remained an unsolved problem.

To address the **compute path challenge**, a separate set of tools provided visibility into application performance.
* **Debuggers and monitoring systems** like TotalView, built on overlay networks like MRNet, offered a top-down view of application state.
* **Performance tools** were generally limited to traditional profiling, which produces high-level aggregates that hide transient anomalies, or tracing, which generates voluminous and unstructured data that is notoriously difficult to analyze offline.
* There was a lack of tools that could provide a **programmable, query-driven** view of performance, forcing developers to engage in painstaking forensic analysis to untangle the root causes of variability.

#### **This Work: A Journey to Generality**

This dissertation documents a research journey that begins by addressing a specific gap in the data path toolkit and culminates in a general-purpose framework that unifies both the data and compute challenges under a single paradigm.

Our work first addresses the challenge of in-situ range partitioning. We propose **CARP**, a system that continuously and adaptively repartitions data based on its observed key distribution as it streams from the application. Beyond enabling efficient range queries, CARP’s adaptive renegotiation mechanism serves as a "proto-OODA loop" (Observe-Orient-Decide-Act)—a distributed control pattern that we revisit and generalize later in this work.

We then context-switch to the seemingly unrelated problem of load imbalance in adaptive mesh refinement (AMR) codes. Through extensive, fine-grained profiling on a dedicated cluster, we discovered that the presenting problem of "load imbalance" was often a symptom of deeper, cross-stack issues—**things masquerading as load imbalance**, such as hardware thermal throttling, driver stalls, and network contention. We concluded that the central challenge was not designing a better load-balancing algorithm, but the fundamental difficulty of **achieving trustworthy, actionable insight in-situ**. The "eBPF revelation" during this study highlighted a path forward: observability needed to be streaming, interactive, lightweight, selective, and, above all, **programmable**.

This insight led to the design of our culminating work, **ORCA**. We realized that a general-purpose, query-driven observability system could be used for *any* in-situ analytics task. ORCA unifies concepts from the database and stream processing worlds—using Apache Arrow as a universal data format and distributed SQL query engines like DataFusion—to create a "sense-making engine" for the entire cluster. It is built on an **"analyze, then persist"** philosophy, providing a programmable fabric that can be used for everything from performance diagnosis to in-situ scientific data analysis, finally breaking down the silos between the data and compute path tools.

#### **Thesis Statement**

By treating both scientific data and performance telemetry as queryable streams within a unified, programmable dataflow framework, the distinct challenges of data management and compute-path optimization in large-scale synchronous applications can be solved with a single, general-purpose methodology.

#### **Overview of Contributions**

This thesis presents three major contributions that progressively develop this unified approach:

* **CARP** fills a critical gap in in-situ data organization by providing the first scalable system for adaptive range partitioning of streaming data, completing the toolkit of fundamental partitioning primitives for in-situ analytics.

* The **AMR Performance Study** develops programmable, empirical workflows for real-world performance diagnosis, demonstrating the necessity of query-driven, full-stack telemetry over traditional approaches and revealing that the core problem is often understanding the problem itself.

* **ORCA** generalizes these insights into a unified, real-time framework for observability and control at cluster scale, providing a programmable and declarative substrate for both data analytics and system optimization that bridges the gap between database systems and HPC.