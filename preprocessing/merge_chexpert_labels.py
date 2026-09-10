import os
import pandas as pd

FINAL_DATASET_DIR = r"C:\Users\vysha\OneDrive\Desktop\prognosx\data\processed\final_dataset"
CHEXPERT_CSV = r"C:\Users\vysha\OneDrive\Desktop\prognosx\data\raw\mimic-cxr-2.0.0-chexpert.csv"

manifest = pd.read_csv(os.path.join(FINAL_DATASET_DIR, "training_manifest.csv"))
chexpert = pd.read_csv(CHEXPERT_CSV)

# Recover study_id per scan from each patient's own order.csv (already saved)
study_id_rows = []
for sid in manifest["subject_id"].unique():
    order_path = os.path.join(FINAL_DATASET_DIR, str(sid), "cxr", "order.csv")
    if os.path.exists(order_path):
        order = pd.read_csv(order_path)
        study_id_rows.append(order[["subject_id", "dicom_id", "study_id"]])

study_ids = pd.concat(study_id_rows, ignore_index=True)

manifest = manifest.merge(study_ids, on=["subject_id", "dicom_id"], how="left")
print("Manifest rows missing study_id after merge:", manifest["study_id"].isna().sum())

labeled = manifest.merge(chexpert, on=["subject_id", "study_id"], how="left")

out_path = os.path.join(FINAL_DATASET_DIR, "training_manifest_labeled.csv")
labeled.to_csv(out_path, index=False)
print(f"Saved {len(labeled)} rows -> {out_path}")
print("Columns:", labeled.columns.tolist())