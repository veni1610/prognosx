"""
Loads and cleans MIMIC-CXR metadata + CheXpert labels, parses study
timestamps, resolves image file paths. Run this first.

Currently scoped to only the patient partitions physically present on
disk (see config.ALLOWED_PATIENT_PREFIXES) — e.g. p10, p11 — so we don't
waste time checking os.path.exists() against rows for partitions we
don't have.
"""
import os
import pandas as pd
import config

def parse_timestamp(row):
    date = str(int(row["StudyDate"]))
    time = str(int(float(row["StudyTime"]))).zfill(6)
    return pd.to_datetime(date + time, format="%Y%m%d%H%M%S", errors="coerce")

def get_patient_prefix(subject_id):
    return "p" + str(subject_id)[:2]

def find_image_path(row):
    subject_id = str(row["subject_id"])
    study_id = str(row["study_id"])
    dicom_id = str(row["dicom_id"])
    p_prefix = "p" + subject_id[:2]
    return os.path.join(
        config.MIMIC_CXR_IMAGE_ROOT,
        p_prefix,
        f"p{subject_id}",
        f"s{study_id}",
        f"{dicom_id}.jpg"
    )

def load_clean_metadata():
    meta = pd.read_csv(config.MIMIC_CXR_METADATA_CSV)
    chexpert = pd.read_csv(config.MIMIC_CXR_CHEXPERT_CSV)

    # Restrict to only the partitions we actually have on disk (e.g. p10, p11)
    # BEFORE the expensive path-existence check, since that's the slow part.
    allowed = getattr(config, "ALLOWED_PATIENT_PREFIXES", None)
    if allowed:
        before = len(meta)
        meta = meta[meta["subject_id"].apply(get_patient_prefix).isin(allowed)]
        print(f"Restricted to {allowed}: {len(meta)} of {before} metadata rows kept")

    meta["timestamp"] = meta.apply(parse_timestamp, axis=1)
    meta = meta.dropna(subset=["timestamp"])
    meta["image_path"] = meta.apply(find_image_path, axis=1)
    meta = meta[meta["image_path"].apply(os.path.exists)]

    merged = meta.merge(
        chexpert, on=["subject_id", "study_id"], how="left", suffixes=("", "_chexpert")
    )
    return merged

def main():
    print("main() started")
    df = load_clean_metadata()
    out_path = os.path.join(config.OUTPUT_DIR, "clean_metadata.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} valid image records with timestamps -> {out_path}")

if __name__ == "__main__":
    main()