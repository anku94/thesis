# CARP — Adaptive In-Situ Range Partitioning

## Relevant Background and Architectural Rationale

  * Prior in-situ approaches were either tightly coupled to the application (hard to adapt and extend) or focused on fast, unordered ingestion (hash partitioning), sacrificing query efficiency.
  * Range queries are critical in scientific analysis, but traditional solutions required expensive post-processing sorts—architecturally at odds with the streaming, in-memory nature of modern HPC I/O.
  * The network-to-storage bandwidth gap and the bursty, append-heavy I/O patterns of checkpointing make streaming, adaptive, one-pass reorganization architecturally optimal.

## Motivation and Context

  * Adaptive range partitioning was the last missing primitive for general in-situ data organization.
  * Scientific datasets are highly skewed and dynamic, demanding solutions that can adjust in real time.

## Approach

  * CARP adaptively reorganizes data during application I/O, discovering and adjusting range partitions on the fly.
  * Operates fully in-situ, without extra passes or reordering after the fact.

## Key Results

  * Delivers near-sorted query performance for range queries, with zero ingestion overhead.
  * Outperforms prior work: up to 5x faster than post-processing and up to 100x lower query latency than in-situ indexing baselines.
  * Robust across extremes of skew and evolving data distributions.

## Broader Impact

  * Completes the set of architectural primitives for in-situ data organization.
  * Introduces the “state-driven adaptive control loop” pattern, a theme carried forward in the thesis.