# Thesis Context Brief

## Overview

PhD thesis by Ankush Jain (CMU ECE, advised by George Amvrosiadis). Thesis argues that BSP efficiency bottlenecks are fundamentally problems of constructing the right views of distributed application state, and proposes ORCA as a programmable observability and control plane.

Three projects, unified by the theme of feedback loops between observation and intervention in BSP systems.

## Project 1: CARP (SC '24) — Data Path

**What it is.** An in-situ streaming range partitioner for scientific data. Ingests data at storage-line rate while producing a partially ordered layout that supports efficient range queries — no post-processing sort needed.

**The feedback loop.** Open-loop. CARP runs renegotiation periodically: ranks summarize their local key distributions, a leader merges them into a global view, and new partition boundaries are broadcast. This runs on a fixed schedule — there's no feedback-driven trigger. It just works because the mechanism is simple and the function is fixed (range partitioning). 5× faster ingestion than prior work, query performance matching a full sort.

**Key property.** Automatic, low-overhead, but fixed-function. CARP can only construct one kind of view (key distribution) and take one kind of action (repartition). No programmability.

## Project 2: AMR Placement (CLUSTER '25) — Compute Path

**What it is.** A study of placement and load-balancing in adaptive mesh refinement codes (Phoebus/Parthenon, Sedov blast wave). Developed CPLX, a hybrid placement policy with a tunable parameter X that interpolates between communication locality (X=0) and load balance (X=100). Up to 21.6% runtime improvement over tuned baselines at 4096 ranks.

**The feedback loop.** Broken/manual. The work required constructing fine-grained views of per-rank, per-timestep telemetry to diagnose performance artifacts. But the infrastructure didn't exist:

- Initial telemetry didn't correlate with expected behavior (R²=0.01). Full-stack debugging revealed fail-slow hardware, driver bugs, MPI tuning issues.
- Each diagnosis iteration required: instrument → run → collect traces → ETL (CSV → pandas → ClickHouse) → analyze → hypothesize → repeat.
- Each artifact took months to diagnose. Fixes typically took days.
- Existing tools were inadequate: profilers lacked granularity, traces were too large and not queryable, formats like OTF2 aren't designed for analytics.

**Key property.** The loop was conceptually closed (observe → diagnose → intervene) but operationally broken — slow, manual, ad-hoc. The programmability was there (SQL queries over telemetry) but only offline after expensive ETL. No real-time feedback.

## Project 3: ORCA (in submission) — Unified

**What it is.** A tree-based overlay network (TBON) for real-time observability and control of BSP applications. Users express views as SQL over telemetry streams (OrcaFlow). Distributed query planning pushes operators down to MPI ranks. Timestep-consistent control via TS2PC.

**The feedback loop.** Closed, programmable, real-time. ORCA unifies what CARP and AMR needed:

- **Observation:** Telemetry collected as columnar timestep dataframes (Arrow), transformed via SQL en route to sinks. Operator pushdown discards 98.5–99.999% of data at source. 1–2% runtime overhead vs 56–81% for existing tracers.
- **Intervention:** TS2PC provides atomic, timestep-consistent control — new flows, probes, parameter updates applied at the same timestep across all ranks.
- **The loop in action:** In an agentic evaluation, an LLM agent localized a performance anomaly (the same bug from the AMR study) in 27 minutes — the same bug that took months manually.

**Key property.** Closed-loop, low-overhead, and programmable. The only column with all three.

## The Thesis Arc

| Property | CARP | AMR | ORCA |
|---|---|---|---|
| Closed-loop | Open-loop (periodic, works fine) | Conceptually closed, operationally broken | Closed, real-time |
| Low overhead | Yes (in-situ, streaming) | No (56–81% tracing overhead) | Yes (1–2% with RDMA + Arrow) |
| Programmable | No (fixed function) | Yes but offline (ad-hoc SQL over ETL'd traces) | Yes, real-time (SQL views on demand) |

**Thesis statement (working):** BSP efficiency is bottlenecked on constructing the right views of distributed application state. Low-latency views are necessary to drive adaptive mechanisms, both automated and manual. ORCA is a programmable TBON for low-latency view construction and intervention.

## Tech Stack

- **TBON:** Three-tier overlay (MPI ranks → Aggregators → Controller)
- **Data:** Apache Arrow columnar format, persisted as timestep+rank-partitioned Parquet
- **Analytics:** Apache DataFusion for distributed query planning, DuckDB + FlightSQL + Grafana for real-time dashboards
- **Transport:** RDMA via Mercury/libfabric
- **Control:** TS2PC (timestep-linked two-phase commit)
- **Interface:** OrcaFlow DSL (SQL transforms chained over streams, routed to sinks)
- **Codebase:** 40K LOC (80% C++, 20% Rust)