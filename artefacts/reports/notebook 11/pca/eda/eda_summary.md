# Notebook 11 gated cross-modal attention EDA summary: pca

This EDA focuses on model behaviour rather than long result tables. It summarises performance, seed stability, validation-to-test transfer, prediction spread, gating, attention, Integrated Gradients attribution, and available baseline comparison.

The strongest arm by mean Spearman was `prot_combined_union` with mean Spearman `0.0609`.

The strongest configuration was `prot_rppa_ccle` with `RNA+CNV+MUT+PROT` for `RUBITECAN (BRD:BRD-K79821389-001-03-5)`, reaching mean Spearman `0.2548`.

Prediction variance diagnostics were not available.

Matched tabular baseline comparison was available for `60` arm-feature rows. The median gated-attention minus baseline Spearman difference was `0.0658`.

## Generated figures

- `Arm-feature performance heatmap`: Shows which modality combinations perform best within each proteomics arm. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pca/figures/eda__arm_feature_mean_spearman_heatmap.png`.
- `Per-fold Spearman distribution`: Shows fold-level spread rather than only mean performance. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pca/figures/eda__per_fold_spearman_box_jitter_by_arm.png`.
- `Top configuration stability`: Shows the strongest configurations with seed variability as uncertainty bars. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pca/figures/eda__top_config_seed_stability.png`.
- `Seed consistency scatter`: Checks whether strong configurations remain strong across random seeds. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pca/figures/eda__seed_consistency_scatter.png`.
- `Validation-to-test transfer`: Checks whether validation Spearman is a useful proxy for held-out performance. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pca/figures/eda__validation_to_test_transfer.png`.
- `Observed versus predicted AUC`: Visualises calibration and ranking behaviour for the best configuration. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pca/figures/eda__best_config_observed_vs_predicted.png`.
- `Residual diagnostic`: Shows whether prediction error changes systematically across observed AUC values. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pca/figures/eda__best_config_residuals.png`.
- `Gate heatmap for best feature sets`: Shows how the fusion model weights each available modality for each arm's best feature set. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pca/figures/eda__gate_heatmap_best_feature_sets.png`.
- `Gate and missingness association`: Checks whether the model downweights modalities as missingness increases. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pca/figures/eda__gate_missingness_spearman_heatmap.png`.
- `Integrated Gradients modality heatmap`: Compares attribution strength assigned to each modality in selected best runs. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pca/figures/eda__integrated_gradients_modality_heatmap.png`.
- `Top Integrated Gradients components`: Shows the strongest representation-level attribution components from selected best runs. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pca/figures/eda__integrated_gradients_top_components.png`.
- `Delta against tabular baseline`: Shows where gated attention improves or underperforms against matched earlier baselines. Saved at `/home/andrija/Desktop/Final Year Project/FYP/artefacts/reports/notebook 11/pca/figures/eda__delta_vs_baseline_heatmap.png`.
