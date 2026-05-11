# Notebook 11 gated cross-modal attention EDA summary: pathway

This EDA focuses on model behaviour rather than long result tables. It summarises performance, seed stability, validation-to-test transfer, prediction spread, gating, attention, Integrated Gradients attribution, and available baseline comparison.

The strongest arm by mean Spearman was `prot_combined_union` with mean Spearman `0.0666`.

The strongest configuration was `prot_ms_ccle_gygi` with `RNA+CNV+MUT+PROT` for `IXAZOMIB (BRD:BRD-K78659596-001-03-9)`, reaching mean Spearman `0.2587`.

Prediction-variance diagnostics were generated for sampled prediction files. The fraction of arm-feature summaries with median prediction-to-response SD ratio below 0.05 was `0.000`, which helps detect configurations that rank weakly because predictions collapse towards a narrow range.

Matched tabular baseline comparison was available for `52` arm-feature rows. The median gated-attention minus baseline Spearman difference was `0.0596`.

## Generated figures

- `Arm-feature performance heatmap`: Shows which modality combinations perform best within each proteomics arm. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pathway/figures/eda__arm_feature_mean_spearman_heatmap.png`.
- `Per-fold Spearman distribution`: Shows fold-level spread rather than only mean performance. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pathway/figures/eda__per_fold_spearman_box_jitter_by_arm.png`.
- `Top configuration stability`: Shows the strongest configurations with seed variability as uncertainty bars. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pathway/figures/eda__top_config_seed_stability.png`.
- `Seed consistency scatter`: Checks whether strong configurations remain strong across random seeds. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pathway/figures/eda__seed_consistency_scatter.png`.
- `Validation-to-test transfer`: Checks whether validation Spearman is a useful proxy for held-out performance. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pathway/figures/eda__validation_to_test_transfer.png`.
- `Observed versus predicted AUC`: Visualises calibration and ranking behaviour for the best configuration. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pathway/figures/eda__best_config_observed_vs_predicted.png`.
- `Residual diagnostic`: Shows whether prediction error changes systematically across observed AUC values. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pathway/figures/eda__best_config_residuals.png`.
- `Prediction variance collapse diagnostic`: Checks whether low performance is associated with near-constant predictions. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pathway/figures/eda__prediction_variance_collapse_scatter.png`.
- `Gate heatmap for best feature sets`: Shows how the fusion model weights each available modality for each arm's best feature set. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pathway/figures/eda__gate_heatmap_best_feature_sets.png`.
- `Gate and missingness association`: Checks whether the model downweights modalities as missingness increases. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pathway/figures/eda__gate_missingness_spearman_heatmap.png`.
- `Best configuration attention matrix`: Shows cross-modal attention for the best overall gated-attention configuration. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pathway/figures/eda__attention_matrix_best_overall_config.png`.
- `Integrated Gradients modality heatmap`: Compares attribution strength assigned to each modality in selected best runs. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pathway/figures/eda__integrated_gradients_modality_heatmap.png`.
- `Top Integrated Gradients components`: Shows the strongest representation-level attribution components from selected best runs. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pathway/figures/eda__integrated_gradients_top_components.png`.
- `Delta against tabular baseline`: Shows where gated attention improves or underperforms against matched earlier baselines. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pathway/figures/eda__delta_vs_baseline_heatmap.png`.
