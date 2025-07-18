# ML scale
- :LlamaScale (blogpost, Llama4 speculation)
- Rahma2024:MLScale (webpage, epochai, notes trends)
- Gratt2024:Llama3Scale

# HPC scale
- Das2023:LargeScale (Gordon Bell award)
- Stock2024:LargeScale (Gordon Bell award)

# HPC Environment
- Lustre: Braam2002
- DAOS: Henne2020
- 2024:Hammerspace
- :VastPlatform
- Glenn2025:NoPFS (use object stores, Glenn Lockwood)

- Frontend vs backend: Gangi2024 (meta paper)
- Pfist2001:Infiniband
- Rowet2022:Slingshot
- Metz2024:UltraEthernet

- HPC GPU importance: DeBar2014, Snell2017
- :TOP500ListJune

- VPIC2.0: Bird2022, mesh codes: Dubey2014 (archetyles)


# CARP-related

## In-situ

- In-situ: Bauer2016
- In-situ taxonomy and review (really good): Child2020
- ADIOS: Gu2018, Eisen2024
- DeltaFS: Zheng2019

## Other

- PebblesDB: Raju2017
- SDS-Sort: Dong2016
- FastBit: Wu2005
- FastQuery: Byna2012
- TritonSort: Rasmu2011
- HykSort: Sunda2013
- Slalom: Olma2017
- Online range partitioning: Ganes2004, Konst2011
- Range queries: Bhara2004

# AMR-related

- AMR: VanS2009
- Applications: VanS2009

## Variability

- Variability: Acun2016 (two works)
- Varbench: Kocol2018
- IO noise: Yildi2017
- System noise: Hoef2010
- Collective tuning at Meta: Gangi2024

## AMR

- AMR Survey: Dubey2014
- Parthenon: Grete2023
- AMReX: Zhang2021
- Meta-Balancer: Menon2012 (when to rebalance)
- Applying graph partitioning: Bhate2011
- Multi-level load-balancing: Bak2018

# ORCA-related

## ML Problems
- TrainCheck: Jiang2025
- XPUTimer: Cui2025
- Direct Telemetry Access: Langl2023

## HPC Tools
- Natar2010 -- does TAU over MRNet
- DynInst: Berna2011
- Wylie2025 (Scalasca, Paravel, ScoreP, Extrae)
- TAU: Shend2006
- SOMA: Yokel2024, maybe Yoken2023
- LLNL Caliper

## Standard Tools
- :eBPF
- :GrafanaDashboard, :ApacheArrow, :ApacheParquet

## In-situ

- Dorie2023 (Colza, elastic in-situ)
- DuckDB: Raasv2019
- Datafusion: Lamb2024
- Mercury: Souma2013

## ScienceSQL

- :TileDB
- Lee2004:MeshSQL
- Kerst2011:SciQL
- Rezae2014:UnstructuredMeshAlgebra

## Uncategorized

- Use Arrow for partle analytics: Liu2022
- Use Arrow for SmartNICs: Ulmer2023
- Do you really need to store all that telemetry? (Klein2024, blog post)
- Fay: declarative dataflow for Windows clusters (Erlin2011:Fay)
- Snicket: declarative query-driven RPC tracing + WASM (Berg2011:Snicket)
- Mach: single-node ingestion engine (like SysX)
- DFTracer (Devar2024)
- TAU 2024 runtime overhead/ML etc: Huck2025:TAU
-- Also does streaming stuff using ADIOS2!!

- Jones2012: "Failure probability increases with scale, so checkpointing becomes more frequent"


## George mentioned
- SysX (may not be published)
- FishStore (?)
- InfluxDB?

## Kaihua mentioned

- Minder (NSDI 2025)
- XPUTimer (Arxiv)
- Aegis: NSDI2025
- SilentErrors: Jiang2025 (OSDI 2025)
- Holmes (NSDI 2025)
- Greyhound (ATC 2025)
- SuperBench (ATC 2024)