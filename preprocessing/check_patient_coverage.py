"""
Quick diagnostic: how many patients have >=2 CXRs (usable for CXR-TFT
temporal sequences) vs only 1 (usable only for classifier training).
Run this AFTER cxr_metadata.py.
"""
import os
import pandas as pd
import config

def main():
    meta_path = os.path.join(config.OUTPUT_DIR, "clean_metadata.csv")
    meta = pd.read_csv(meta_path)

    counts = meta.groupby("subject_id")["study_id"].nunique()

    multi_scan = counts[counts >= 2]
    single_scan = counts[counts == 1]

    print(f"Total unique patients: {len(counts)}")
    print(f"Patients with >=2 CXR studies (usable for temporal model): {len(multi_scan)}")
    print(f"Patients with exactly 1 CXR study (usable only for classifier): {len(single_scan)}")
    print()
    print("Distribution of scan counts among multi-scan patients:")
    print(multi_scan.value_counts().sort_index())

    out_path = os.path.join(config.OUTPUT_DIR, "multi_scan_patient_ids.csv")
    multi_scan.to_csv(out_path, header=["num_studies"])
    print(f"\nSaved {len(multi_scan)} usable subject_ids -> {out_path}")

if __name__ == "__main__":
    main()