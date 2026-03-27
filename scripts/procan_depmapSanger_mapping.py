import re
import numpy as np
import pandas as pd
from pathlib import Path

PROCAN_AVG_TSV = Path("data/procan_depmapSanger/raw/20250211/Protein_matrix_averaged_20250211.tsv")
DEPMAP_META_CSV = Path("data/depmap/raw/Subtype_Matrix_Public_25Q3_subsetted.csv")

PROCAN_PROCESSED_DIR = Path("data/procan_depmapSanger/processed")
PROCAN_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

MAPPING_CSV = PROCAN_PROCESSED_DIR / "procan_depmap_id_mapping.csv"
UNMAPPED_TXT = PROCAN_PROCESSED_DIR / "procan_unmapped_cell_lines.txt"

PROTEOMICS_MATRIX_PARQUET = PROCAN_PROCESSED_DIR / "procan_proteomics_depmap_index.parquet"
PROTEOMICS_MATRIX_CSV = PROCAN_PROCESSED_DIR / "procan_proteomics_depmap_index.csv"

PROTEOMICS_WITH_METADATA_PARQUET = PROCAN_PROCESSED_DIR / "procan_proteomics_depmap_with_metadata.parquet"
PROTEOMICS_WITH_METADATA_CSV = PROCAN_PROCESSED_DIR / "procan_proteomics_depmap_with_metadata.csv"

META_COLS = [
    "depmap_id",
    "cell_line_display_name",
    "lineage_1",
    "lineage_2",
    "lineage_3",
    "lineage_6",
    "lineage_4",
]

def normalise_cell_line_name(x: str) -> str:
    x = "" if x is None else str(x)
    x = x.upper().strip()
    return re.sub(r"[^A-Z0-9]+", "", x)

raw = pd.read_csv(PROCAN_AVG_TSV, sep="\t", dtype=str, low_memory=False)
raw = raw.rename(columns={raw.columns[0]: "row_id"}).set_index("row_id")

symbol_row = raw.loc["symbol"] if "symbol" in raw.index else None
to_drop = [r for r in ["symbol", "model_name", "model_id"] if r in raw.index]
data = raw.drop(index=to_drop, errors="ignore")

meta_cols = []
for c in data.columns:
    s = data[c].astype(str)
    if (s.str.match(r"^SIDM\d+$").mean() > 0.8) or (c.lower() in ["model_id", "model_name"]):
        meta_cols.append(c)

X = data.drop(columns=meta_cols, errors="ignore").apply(pd.to_numeric, errors="coerce")

if symbol_row is not None:
    mapped = symbol_row.reindex(X.columns)
    mapped = mapped.where(mapped.notna() & (mapped.astype(str) != ""), other=X.columns)
    X.columns = mapped.astype(str)
    X = X.groupby(level=0, axis=1, sort=False).mean()

print("ProCan matrix:", X.shape)
print("Missing fraction:", float(np.isnan(X.values).mean()))

dep = pd.read_csv(DEPMAP_META_CSV, usecols=META_COLS, low_memory=False).dropna(subset=["depmap_id", "cell_line_display_name"])
dep = dep.drop_duplicates("depmap_id").copy()
dep["match_key"] = dep["cell_line_display_name"].map(normalise_cell_line_name)
dep = dep.drop_duplicates("match_key", keep="first")

pro = pd.DataFrame({"model_name": X.index.astype(str)})
pro["match_key"] = pro["model_name"].map(normalise_cell_line_name)

mapping = pro.merge(dep[META_COLS + ["match_key"]], on="match_key", how="left")
mapping.to_csv(MAPPING_CSV, index=False)

mapped_rate = mapping["depmap_id"].notna().mean()
print(f"Mapped rows: {mapped_rate*100:.1f}%")

unmapped = mapping.loc[mapping["depmap_id"].isna(), "model_name"].head(200).tolist()
if unmapped:
    UNMAPPED_TXT.write_text("\n".join(unmapped), encoding="utf-8")

mapping_ok = mapping.dropna(subset=["depmap_id"]).copy()

X_mapped = X.loc[mapping_ok["model_name"].values].copy()
X_mapped.index = mapping_ok["depmap_id"].astype(str).values
if X_mapped.index.duplicated().any():
    X_mapped = X_mapped.groupby(level=0, sort=False).mean()

X_mapped.index.name = "depmap_id"
X_mapped.to_parquet(PROTEOMICS_MATRIX_PARQUET)
X_mapped.reset_index().to_csv(PROTEOMICS_MATRIX_CSV, index=False)

meta_aligned = dep.set_index("depmap_id").reindex(X_mapped.index).reset_index()
proteomics_df = X_mapped.reset_index()
out = meta_aligned.merge(proteomics_df, on="depmap_id", how="right")

protein_cols = [c for c in out.columns if c not in META_COLS]
out = out[META_COLS + protein_cols]

out.to_parquet(PROTEOMICS_WITH_METADATA_PARQUET, index=False)
out.to_csv(PROTEOMICS_WITH_METADATA_CSV, index=False)

print("Proteomics (DepMap index):", X_mapped.shape)
print("Proteomics + metadata:", out.shape)
print(out[META_COLS].head(10).to_string(index=False))
