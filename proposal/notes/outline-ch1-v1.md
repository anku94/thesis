# Introduction

## Motivation and Scope

* Scientific and ML workloads at scale generate immense data on both the I/O and observability paths.
* The dominant model has been “collect and post-process”—write data to storage, then analyze.
* Modern scale strains this approach: high I/O costs, slow insight, and underutilized results.
* Motivates the search for fundamentally new paradigms in data and performance management.

## Status Quo: BSP, Checkpointing, and In-Situ Processing

* Bulk Synchronous Parallel (BSP): clusters progress in globally synchronized compute/I/O phases.
* Checkpointing and trace collection are essential, but I/O and synchronization costs rise with scale.
* In-situ analytics emerged to address the “persist-then-analyze” bottleneck:

  * Early in-situ work focused on tightly coupled libraries (e.g., ParaView Catalyst), often limited to scripted visualization or filtering.
  * Loosely coupled approaches (e.g., ADIOS, DataSpaces) enabled co-processing but added complexity and network dependencies.
  * Overlay networks (MRNet, LDMS) provided scalable reduction but limited programmability, mostly used for monitoring.
  * In-situ indexing advanced with systems like DeltaFS (hash partitioning), but left adaptive range partitioning unsolved.
* Most in-situ systems were point solutions: valuable, but narrow in scope, with limited programmability or generality.

## Gaps and the Journey to Generality

* On the data path, the available toolkit for in-situ analytics was incomplete: most efforts focused on specific tasks like visualization or compression, leaving open challenges such as adaptive range partitioning.
* On the compute path, the prevailing struggle was diagnosing and fixing performance, widely understood as a load balancing problem but plagued by noisy telemetry and insufficient tools.
* This thesis began by treating these as two separate research problems. Only through empirical systems work did it become clear that both were instances of a deeper, more general challenge: organizing and processing streaming data for both insight and control.

## Thesis Statement

* *Thesis:* Streaming, programmable analytics and control can unify and solve both data and compute challenges in synchronized cluster computing.

## Overview of Contributions

* **CARP:** Fills the last major gap in in-situ data organization: adaptive range partitioning of streaming data.
* **CPLX/AMR:** Develops programmable, empirical workflows and tunable placement for real-world performance diagnosis and tuning.
* **ORCA:** Generalizes these insights into a unified, real-time framework for observability and control at cluster scale.
