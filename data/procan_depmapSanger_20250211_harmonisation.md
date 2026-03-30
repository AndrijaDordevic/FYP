# ProCan–DepMapSanger Proteomics Harmonisation to DepMap IDs

## Objective  
To standardise the ProCan–DepMapSanger proteomics matrix and align it to DepMap identifiers (`depmap_id`), enabling direct, reproducible joins with DepMap omics (RNA, CNV, mutations) and drug response (e.g., PRISM) using a single canonical key.

## Why ProCan–DepMapSanger is included (and how it will be used)  
The CCLE MS proteomics (Gygi/DepMap-CCLE) arm offers deep protein quantification but typically covers far fewer cell lines, which can limit statistical power and model stability in proteogenomic drug response prediction. ProCan–DepMapSanger provides substantially higher cell line coverage, making it a strong candidate proteomics backbone when sample size is the primary bottleneck.

In this project, ProCan–DepMapSanger is therefore used as a **comparison proteomics arm** rather than a silent replacement. After harmonisation, it can be benchmarked against the CCLE MS proteomics arm under the same lineage-aware, leakage-safe evaluation protocol. This allows an explicit, evidence-based decision on whether the increased sample coverage (ProCan) outweighs any trade-offs in proteomic depth or missingness relative to CCLE MS.

## Rationale  
ProCan–DepMapSanger proteomics is not natively keyed by DepMap identifiers, whereas the remainder of the pipeline (DepMap metadata, RNA, CNV, mutations, PRISM response, and lineage-aware evaluation) depends on `depmap_id` as the canonical join key. This harmonisation step therefore (i) enforces a single identifier backbone to prevent ambiguous joins, (ii) produces auditable mapping artefacts for transparency and reproducibility, and (iii) standardises the proteomics feature space so downstream modelling is consistent and leakage-safe when preprocessing is performed fold-wise.

## Inputs  
- **ProCan averaged proteomics (raw):** `data/procan_depmapSanger/raw/20250211/Protein_matrix_averaged_20250211.tsv`  
- **DepMap metadata (raw):** `data/depmap/raw/Subtype_Matrix_Public_25Q3_subsetted.csv`  
  Required fields: `depmap_id`, `cell_line_display_name`, `lineage_1`, `lineage_2`, `lineage_3`, `lineage_4`, `lineage_6`.

## Method  
1. **Matrix ingestion and cleaning**  
   The ProCan TSV is loaded in a type-robust manner. Non-assay annotation rows (e.g., `symbol`, `model_name`, `model_id`) are removed if present. Any non-proteomic identifier-like columns (e.g., predominantly `SIDM#######`) are excluded. Remaining entries are coerced to numeric, preserving missing values.

2. **Protein identifier standardisation (optional)**  
   If a `symbol` annotation row is present, protein identifiers are mapped to gene symbols where available. Duplicate gene symbols are collapsed by mean to ensure a single feature per gene.

3. **DepMap ID mapping via standardised name keys**  
   ProCan row labels (model names) are mapped to DepMap using `cell_line_display_name`. Both are normalised (uppercase, whitespace trimmed, non-alphanumeric removed) to form a stable `match_key`. A left join assigns `depmap_id` where a match is found; DepMap duplicate keys are resolved by retaining the first occurrence to enforce a one-to-one mapping.

4. **Reindexing and collision handling**  
   The proteomics matrix is filtered to mapped entries and reindexed by `depmap_id`. If multiple ProCan rows map to the same `depmap_id`, values are aggregated by mean to retain one row per DepMap cell line.

5. **Metadata augmentation for reporting and compatibility**  
   A DepMap-style table is produced by joining mapped proteomics with DepMap metadata fields (display name and lineage levels), yielding a single table with metadata columns followed by protein/gene features.

## Outputs (written to `data/procan_depmapSanger/processed/`)  
- **Mapping audit:** `procan_depmap_id_mapping.csv`  
- **Unmapped examples:** `procan_unmapped_cell_lines.txt` (first 200 unmapped names for manual review)  
- **DepMap-indexed proteomics matrix (preferred modelling input):**  
  - `procan_proteomics_depmap_index.parquet`  
  - `procan_proteomics_depmap_index.csv`  
  Structure: index/first column = `depmap_id`, columns = proteins/genes, values = abundances.  
- **DepMap-style proteomics (metadata + features):**  
  - `procan_proteomics_depmap_with_metadata.parquet`  
  - `procan_proteomics_depmap_with_metadata.csv`  
  Structure: `depmap_id`, `cell_line_display_name`, `lineage_*`, then proteomics features.

## Verification criteria  
The script reports: cleaned matrix shape, missing-value fraction, mapping rate (% rows assigned a `depmap_id`), and final output shapes. Successful harmonisation is indicated by (i) high mapping rate, (ii) unique `depmap_id` index after collision handling, and (iii) consistent metadata alignment for mapped cell lines.

## Notes  
This procedure performs name-based alignment and will not resolve all aliases. Unmapped entries are explicitly exported for traceable manual remediation or future replacement with an authoritative crosswalk (e.g., SIDM↔DepMap mapping) where available.

