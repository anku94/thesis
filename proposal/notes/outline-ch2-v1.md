# Background and Landscape

## The BSP Paradigm and Synchronized Cluster Computing

* What is BSP? Why is it foundational for both HPC and large-scale ML?
* Timestepped execution, collectives, and synchronization barriers.
* Impact on application design: sensitivity to stragglers and the importance of uniform progress.

## Anatomy of Modern Clusters

* Cluster resources: nodes, memory hierarchies, accelerators (e.g., GPUs).
* **Networking:**

  * HPC: specialized high-speed fabrics (e.g., InfiniBand, Aries) for collectives, plus Ethernet control networks.
  * ML clusters: backend networks for data, frontend for orchestration.
* Storage infrastructure: parallel filesystems (Lustre, GPFS, BeeGFS), burst buffers, SSD tiers.

## Data Movement and I/O Challenges

* Bursty checkpointing and collective I/O phases in scientific apps.
* The network/storage bandwidth gap as a persistent architectural problem.
* Checkpointing and trace collection as stressors for both storage and system performance.
* The difference between data written for analysis (HPC) and for recoverability (ML).

## In-Situ Analytics: Community Drivers and Status Quo

* Traditional “persist-then-analyze” model and its breakdown at scale.
* Why in-situ emerged: reducing time-to-insight, bandwidth needs, and storage costs.
* Overview of major in-situ paradigms:

  * Tightly coupled: libraries embedded in simulation.
  * Loosely coupled: co-processing with staging/burst nodes.
  * Overlay networks: aggregation and scalable monitoring.
  * In-situ indexing: hash-based (DeltaFS), range (missing).
* Limitations of each and the context for new approaches.

## Scientific Code Ecosystem

* Landscape of open-source and institutional codes: how science gets done at scale.
* **VPIC:** what it is, scientific significance, I/O demands.
* **AMR codes:** (e.g., Parthenon, FLASH, Enzo) for multiscale, adaptive modeling.
* Other representative codes and domains (brief nod to climate, molecular dynamics, etc.).
* Common challenges: data volumes, run duration, complexity, and the resulting analysis needs.