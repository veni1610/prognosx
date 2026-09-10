"""
Checks ICU vs. likely-ward composition of your p10/p11 cohort, using only
files already in final_dataset — no new MIMIC-IV extraction needed.

Logic: chartevents in MIMIC-IV is ICU-sourced. An admission with zero (or
very few) chartevents rows is very likely a ward-only stay with little to
no vitals coverage. This is a proxy, not a definitive ICU flag (you'd need
icustays.csv linked by hadm_id for that), but it directly tells you what
matters for feature engineering: how much real vitals data you'll actually
have per admission.
"""
import os
import pandas as pd

FINAL_DATASET_DIR = r"C:\Users\vysha\OneDrive\Desktop\prognosx\data\processed\final_dataset"
LOW_COVERAGE_THRESHOLD = 5  # admissions with fewer chartevents rows than this are flagged as likely ward-only

def main():
    subject_dirs = [d for d in os.listdir(FINAL_DATASET_DIR)
                    if os.path.isdir(os.path.join(FINAL_DATASET_DIR, d))]

    rows = []
    for sid in subject_dirs:
        patient_dir = os.path.join(FINAL_DATASET_DIR, sid)
        chart_path = os.path.join(patient_dir, "clinical", "chartevents.csv")
        adm_path = os.path.join(patient_dir, "clinical", "admissions.csv")

        if not os.path.exists(adm_path):
            continue

        adm = pd.read_csv(adm_path)
        chart = pd.read_csv(chart_path, low_memory=False) if os.path.exists(chart_path) else pd.DataFrame()

        for _, adm_row in adm.iterrows():
            hadm_id = adm_row["hadm_id"]
            n_chart = 0
            if not chart.empty and "hadm_id" in chart.columns:
                n_chart = (chart["hadm_id"] == hadm_id).sum()

            rows.append({
                "subject_id": sid,
                "hadm_id": hadm_id,
                "n_chartevents_rows": n_chart,
                "likely_icu": n_chart >= LOW_COVERAGE_THRESHOLD,
            })

    df = pd.DataFrame(rows)
    out_path = os.path.join(FINAL_DATASET_DIR, "icu_ward_composition.csv")
    df.to_csv(out_path, index=False)

    total = len(df)
    likely_icu = df["likely_icu"].sum()
    likely_ward = total - likely_icu

    print(f"Total admissions checked: {total}")
    print(f"Likely ICU (>= {LOW_COVERAGE_THRESHOLD} chartevents rows): {likely_icu} ({100*likely_icu/total:.1f}%)")
    print(f"Likely ward/low-coverage (< {LOW_COVERAGE_THRESHOLD} rows): {likely_ward} ({100*likely_ward/total:.1f}%)")
    print(f"\nMedian chartevents rows per admission: {df['n_chartevents_rows'].median()}")
    print(f"Admissions with ZERO chartevents rows: {(df['n_chartevents_rows'] == 0).sum()}")
    print(f"\nSaved per-admission breakdown -> {out_path}")

if __name__ == "__main__":
    main()