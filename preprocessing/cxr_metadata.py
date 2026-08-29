"""
Loads and cleans MIMIC-CXR metadata + CheXpert labels, parses study
timestamps, resolves image file paths. Run this first.
"""
import os
import pandas as pd
import config

def parse_timestamp(row):
    date = str(int(row["StudyDate"]))
    time = str(int(float(row["StudyTime"]))).zfill(6)
    return pd.to_datetime(date + time, format="%Y%m%d%H%M%S", errors="coerce")

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

    meta["timestamp"] = meta.apply(parse_timestamp, axis=1)
    meta = meta.dropna(subset=["timestamp"])
    meta["image_path"] = meta.apply(find_image_path, axis=1)
    meta = meta[meta["image_path"].apply(os.path.exists)]

    merged = meta.merge(
        chexpert, on=["subject_id", "study_id"], how="left", suffixes=("", "_chexpert")
    )
    return merged

def main():
    df = load_clean_metadata()
    out_path = os.path.join(config.OUTPUT_DIR, "clean_metadata.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} valid image records with timestamps -> {out_path}")

if __name__ == "__main__":
    main()