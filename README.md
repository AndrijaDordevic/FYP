# Proteogenomic Fusion Networks for Interpretable Cancer Drug Response Prediction

## Digital Artefact Usage and Reproducibility Guide

This repository provides the source code, notebooks, environment files, generated artefacts, and supporting outputs for the final year project **Proteogenomic Fusion Networks for Interpretable Cancer Drug Response Prediction**.

The project is organised as a reproducible notebook-based experimental pipeline. The notebooks should normally be executed in numerical order because later notebooks depend on aligned datasets, response tables, feature registries, cached transformations, benchmark outputs, or configuration decisions produced by earlier notebooks.

## Repository and Contact Details

The project repository is available at:

[https://github.com/AndrijaDordevic/FYP](https://github.com/AndrijaDordevic/FYP)

For questions about the artefact or reproducibility instructions, contact:

[andrija.dordevic.23@um.edu.mt](mailto:andrija.dordevic.23@um.edu.mt)

## Project Structure

The submitted artefact contains the project notebooks, generated artefacts, environment files, scripts, metadata, reports, and supporting outputs. The expected structure is shown below.

```text
FYP/
|
|-- .venv/                  # Local main virtual environment, not normally committed
|-- .venv_captum/           # Local Captum virtual environment, not normally committed
|
|-- artefacts/
|   |-- aligned/
|   |-- cache/
|   |-- cleaned/
|   |-- metadata/
|   |-- reports/
|
|-- data/
|-- scripts/
|
|-- 01_ingestion_alignment_with_EDA.ipynb
|-- 02_harmonisation_and_canonical_indices.ipynb
|-- 03a_proteomics_backbone_comparison_lfc.ipynb
|-- 03b_proteomics_backbone_comparison_auc.ipynb
|-- 04_imputation_bakeoff.ipynb
|-- 05_deep_imputation.ipynb
|-- 06_remasker_prot.ipynb
|-- 07_not_miwae_prot.ipynb
|-- 08_taskaware_joint_imputation_prediction.ipynb
|-- 09_missingness_threshold_sensitivity.ipynb
|-- 10_string_gat_benchmark.ipynb
|-- 11_gated_cross_modal_attention.ipynb
|-- 12_gated_attention_revised.ipynb
|
|-- requirements-captum.txt
|-- requirements.txt
```

The `artefacts/` directory contains generated outputs such as aligned omics matrices, canonical response tables, metadata, benchmark metrics, cached fold-safe transformations, imputation outputs, reports, figures, model diagnostics, and interpretation files. These artefacts are produced by the notebooks and are used to avoid repeating expensive computations unnecessarily.

## Python Environments

Two Python environments are used. The main environment is used for most notebooks, while a separate Captum environment is used for notebooks that require Captum-based neural interpretability or related dependencies.

| Notebook range | Required environment |
|---|---|
| Notebooks 1 to 6 | Main virtual environment, referred to as `.venv` |
| Notebooks 7 to 9 | Captum virtual environment, referred to as `.venv_captum` |
| Notebooks 10 to 12 | Main virtual environment, referred to as `.venv` |

The main environment can be created using `requirements.txt`. The Captum environment can be created using `requirements-captum.txt`. Exact package versions are provided in the submitted environment files.

## Creating the Main Environment

Create the main environment from the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

After installation, the environment can be registered as a Jupyter kernel if required:

```bash
python -m ipykernel install --user --name fyp-main --display-name "FYP Main"
```

This kernel should be used for Notebooks 1 to 6 and Notebooks 10 to 12.

## Creating the Captum Environment

Notebooks 7, 8, and 9 should be run using the Captum environment. Create the Captum environment from the project root:

```bash
python3 -m venv .venv_captum
source .venv_captum/bin/activate
pip install --upgrade pip
pip install -r requirements-captum.txt
```

The Captum environment can also be registered as a separate Jupyter kernel:

```bash
python -m ipykernel install --user --name fyp-captum --display-name "FYP Captum"
```

When opening Notebooks 7, 8, and 9, select the `FYP Captum` kernel.

## Running the Project from Existing Artefacts

If the submitted `artefacts/` folder is retained, many notebooks can reuse cached outputs and previously generated intermediate files. This is the recommended approach when inspecting the project, checking outputs, or re-running selected later-stage experiments.

The general procedure is:

1. Open the `FYP/` project root folder in the chosen development environment.
2. Activate the correct Python environment for the notebook being inspected.
3. Open the notebook in Jupyter, JupyterLab, VS Code, or another compatible notebook interface.
4. Select the appropriate kernel:
   - `FYP Main` for Notebooks 1 to 6 and 10 to 12.
   - `FYP Captum` for Notebooks 7 to 9.
5. Run the notebook cells in order.

The notebooks include caching and checkpointing logic where relevant. This allows expensive computations to resume from previously completed folds, drugs, seeds, feature sets, proteomics arms, or model configurations instead of starting every run from the beginning.

## Running the Project from Scratch

To regenerate the project outputs from scratch, delete the existing `artefacts/` folder and then run the notebooks sequentially from Notebook 1 onwards.

```bash
rm -rf artefacts/
```

After deleting the artefacts folder, run the notebooks in the following order:

1. `01_ingestion_alignment_with_EDA.ipynb`  
   Data ingestion, alignment, Track 1 and Track 2 cohort construction, and exploratory diagnostics.

2. `02_harmonisation_and_canonical_indices.ipynb`  
   Canonical DepMap ID harmonisation, cell index construction, PRISM long-table creation, and gene-index construction.

3. `03a_proteomics_backbone_comparison_lfc.ipynb`  
   LFC benchmark, proteomics-arm comparison, modality ablations, and baseline evaluation.

4. `03b_proteomics_backbone_comparison_auc.ipynb`  
   AUC benchmark, endpoint comparison, proteomics-arm comparison, and primary-target selection.

5. `04_imputation_bakeoff.ipynb`  
   Classical imputation bake-off.

6. `05_deep_imputation.ipynb`  
   Deep denoising-autoencoder imputation.

7. `06_remasker_prot.ipynb`  
   ReMasker-style proteomics reconstruction.

8. `07_not_miwae_prot.ipynb`  
   not-MIWAE proteomics imputation, using the Captum environment.

9. `08_taskaware_joint_imputation_prediction.ipynb`  
   Task-aware joint imputation and prediction, using the Captum environment.

10. `09_missingness_threshold_sensitivity.ipynb`  
    Missingness threshold sensitivity, using the Captum environment.

11. `10_string_gat_benchmark.ipynb`  
    STRING-GAT graph benchmark.

12. `11_gated_cross_modal_attention.ipynb`  
    Initial gated cross-modal attention experiment.

13. `12_gated_attention_revised.ipynb`  
    Revised gated cross-modal attention experiment.

The notebooks should not be run out of order when regenerating outputs from scratch, because later notebooks depend on artefacts created earlier in the pipeline.

## Important Execution Notes

The project uses fixed random seeds and fold-safe preprocessing. Any transformation that learns statistics from the data, including imputation, scaling, PCA, feature selection, learned compression, or representation fitting, must be fitted only on the training fold and then applied to the validation fold. This rule is already implemented in the notebooks and should not be bypassed when modifying or re-running the pipeline.

Some notebooks are computationally expensive, particularly those involving imputation grids, graph models, neural fusion, repeated seeds, multiple drugs, and multiple proteomics arms. For this reason, the artefact uses cached intermediate outputs and checkpoint files. If a run is interrupted, the notebook can usually be restarted and will skip configurations that have already been completed.

## Expected Main Outputs

After running the full pipeline, the main outputs are stored under `artefacts/`. These include:

- Aligned Track 1 and Track 2 omics matrices.
- `cell_index.parquet`, `prism_long.parquet`, and `gene_index.parquet`.
- Release-lock and metadata files.
- Proteomics coverage and missingness reports.
- Out-of-fold benchmark metrics and predictions.
- Imputation and reconstruction bake-off summaries.
- Missingness threshold sensitivity outputs.
- STRING-GAT diagnostics and graph interpretation outputs.
- Gated attention outputs, gate weights, attention matrices, and prediction diagnostics.
- SHAP, Integrated Gradients, ranked-feature, and pathway-enrichment outputs.
- Figures and reports used for the dissertation evaluation chapter.