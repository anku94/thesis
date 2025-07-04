# ORCA — Generalizing Observability and Control

## Background and Motivation

  * Lessons from CARP and AMR revealed the need for a general, programmable framework for both analytics and real-time control in large clusters.
  * Existing tools provided either narrow observability, limited programmability, or ad-hoc steering—none delivered unified, declarative, scalable control.

## Approach and Architecture

  * ORCA introduces a decoupled overlay network: application, aggregators, and controller communicate via high-performance RPC.
  * Built on distributed query planning (Apache DataFusion) for SQL-driven, in-memory analytics on streaming telemetry.
  * Real-time control via a Timestep-Linked Two-Phase Commit (TS2PC) protocol ensures consistent, synchronized updates across all ranks.

## Key Results and Capabilities

  * Demonstrates scalable, low-overhead analytics at line-rate bandwidths, enabling “analyze-then-persist” at cluster scale.
  * Makes dynamic, cluster-wide control practical—enabling online tuning, interactive workflows, and safe application reconfiguration in situ.
  * Provides a declarative, extensible substrate for both scientific introspection and systems-level observability.

## Remaining Work and Timeline

  * TODO

## Broader Impact

  * ORCA subsumes fragmented observability and steering solutions under a unified, data-centric paradigm.
  * Establishes the general, programmable control loop as a foundational primitive for future HPC and ML systems.
