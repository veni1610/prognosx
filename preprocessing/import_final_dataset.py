import os, shutil
import pandas as pd

SRC = r"D:\veni_maj_proj\final_dataset"
DST = r"C:\Users\vysha\OneDrive\Desktop\prognosx\data\processed\final_dataset"
ALLOWED_PREFIXES = ("10", "11")  # first 2 digits of subject_id

os.makedirs(DST, exist_ok=True)

copied = 0
for sid in os.listdir(SRC):
    src_patient = os.path.join(SRC, sid)
    if not os.path.isdir(src_patient):
        continue
    if sid[:2] in ALLOWED_PREFIXES:
        shutil.copytree(src_patient, os.path.join(DST, sid), dirs_exist_ok=True)
        copied += 1

print(f"Copied {copied} patient folders -> {DST}")

# Also filter the manifest CSVs so they match
for fname in ("training_manifest.csv", "scan_clinical_coverage.csv", "final_cohort_summary.csv"):
    fpath = os.path.join(SRC, fname)
    if os.path.exists(fpath):
        df = pd.read_csv(fpath)
        df = df[df["subject_id"].astype(str).str[:2].isin(ALLOWED_PREFIXES)]
        df.to_csv(os.path.join(DST, fname), index=False)
        print(f"{fname}: kept {len(df)} rows")
    else:
        print(f"WARNING: {fname} not found at {fpath}")