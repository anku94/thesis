HPC Applications Landscape: A Systems-Centric Taxonomy

I. Execution Model and Scale
	•	Bulk Synchronous Parallel (BSP): timestepped compute phases separated by barriers; natural fit for structured physics codes.
	•	Single Program Multiple Data (SPMD): all ranks run the same code on different partitions.
	•	Job scale: large runs span tens to hundreds of thousands of CPUs or thousands of GPUs; extreme-scale simulations run for weeks to months.
	•	Checkpoint/restart: periodic durable I/O for fault tolerance, tightly coupled to simulation cadence.

II. Application Categories

This organizes codes by dominant computation and communication patterns.
	•	Structured Grid Codes
	•	Examples: climate models (CESM, WRF), CFD (OpenFOAM), combustion (S3D).
	•	Data model: N-dimensional arrays, structured mesh, stencil computation.
	•	Challenges: halo exchange, nearest-neighbor comms, I/O from block-partitioned data.
	•	Unstructured Mesh / Finite Element Codes
	•	Examples: deal.II, MFEM, Nek5000.
	•	Data model: sparse graphs, pointer-heavy structures, indirect memory accesses.
	•	Challenges: irregular comms, complex partitioning, poor cache utilization.
	•	Adaptive Mesh Refinement (AMR)
	•	Examples: BoxLib, FLASH, Enzo, VPIC.
	•	Data model: tree-structured or block-structured refinement hierarchy.
	•	Challenges: load balancing, metadata movement, dynamic repartitioning, irregular I/O.
	•	Particle Codes
	•	Examples: PIC codes (VPIC, OSIRIS), N-body (GADGET), MD (LAMMPS).
	•	Data model: SoA particle arrays, spatial bins, sometimes hybrid grid+particle.
	•	Challenges: dynamic memory use, fine-grained locality, scatter/gather comms.
	•	Dense Linear Algebra (HPC DNNs, quantum chemistry, tensor codes)
	•	Examples: QCD codes (MILC), large-scale DNNs, quantum simulation.
	•	Data model: large dense tensors or matrices, often batched.
	•	Challenges: high-bandwidth/low-latency collectives, strong scaling to many GPUs.
	•	Sparse Linear Algebra / Solvers
	•	Common to nearly all above categories (preconditioners, GMRES, multigrid).
	•	Data model: sparse matrices (CSR, blocked, etc.).
	•	Challenges: load imbalance, fine-grained irregularity, global synchrony.

III. Common System Bottlenecks and Patterns
	•	Communication
	•	Dominated by MPI_Allreduce, MPI_Barrier, halo exchanges.
	•	Sensitivity to tail latencies; long global synchronizations every timestep.
	•	I/O
	•	Periodic global checkpoints; bursts of TB-scale I/O.
	•	Heavy use of parallel filesystems (Lustre, GPFS), often inefficiently.
	•	Metadata and small file explosion with AMR or ensemble runs.
	•	Memory & NUMA
	•	High per-rank memory pressure; NUMA effects dominate on-node locality.
	•	Memory affinity often hand-tuned via numactl, MPI rank placement, custom allocators.
	•	Scheduling & Placement
	•	Applications rely on whole-node allocation; tightly control core/thread binding.
	•	Sensitivity to node topology (fabric distance, GPU affinity, NIC bandwidth).
	•	Strong preference for homogeneous, predictable resource behavior.

IV. Emerging Challenges
	•	Heterogeneity
	•	CPU + GPU asymmetry; some physics still on CPU, others ported to GPU.
	•	Split execution models: CPU for control, GPU for kernel launches.
	•	Multi-physics Coupling
	•	Codes that combine e.g., hydrodynamics + gravity + radiation + particles.
	•	Challenge: composition of solvers with different timestep requirements.
	•	Data Movement Dominance
	•	Simulations produce PB-scale data; analysis requires in-situ or co-scheduled post-processing.
	•	Storage and bandwidth now constrain science more than FLOPs.
	•	Observability, Debugging, Tuning
	•	Very limited live introspection; manual telemetry and tracing.
	•	Probing perturbs execution; performance bugs are workload- and scale-dependent.

V. Representative Examples
	•	Provide 3–4 brief examples mapping to the taxonomy:
	•	VPIC: Particle-in-cell plasma physics; 100k+ cores; hybrid particle-grid.
	•	FLASH: AMR hydrodynamics; block-structured hierarchy; checkpoint-heavy.
	•	GTC: gyrokinetic particle simulation; FFTs + particles; heavy collectives.
	•	Exascale ML training: Megatron/GPT; AllReduce-heavy; DDP + pipeline parallel.

# Compressed

II. Application Archetypes: Decomposition and Work Assignment

At scale, HPC applications are defined by how they decompose a physical problem and distribute work across many compute nodes. Most fall into one of three broad classes:

1. Particle-Based Codes

Simulate large numbers of discrete entities (particles, molecules, agents) that move and interact.
Work decomposition: spatial binning; assign particles in a region to each worker.
Systems note: VPIC is a canonical example. Fine-grained locality, dynamic memory use, irregular comms.

2. Grid-Based Codes

Solve PDEs on structured or adaptive meshes—space is discretized into cells.
Work decomposition: partition grid blocks or mesh elements across workers.
Systems note: AMR codes like FLASH use dynamic refinement, which introduces load imbalance and metadata-heavy coordination.

3. Dense/Tensor Workloads (briefly)

Operate on large dense matrices or tensors—common in ML and dense physics.
Work decomposition: chunk matrices/tensors or pipeline layers.
Systems note: Not our focus. These codes are bandwidth- and collective-bound, often GPU-heavy.