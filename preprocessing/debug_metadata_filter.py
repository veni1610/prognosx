import pandas as pd
import config
from preprocessing.cxr_metadata import get_patient_prefix, parse_timestamp, find_image_path
import os

meta = pd.read_csv(config.MIMIC_CXR_METADATA_CSV)
print('Total metadata rows:', len(meta))

allowed = getattr(config, 'ALLOWED_PATIENT_PREFIXES', None)
print('ALLOWED_PATIENT_PREFIXES:', allowed)

if allowed:
    meta_filtered = meta[meta['subject_id'].apply(get_patient_prefix).isin(allowed)]
    print('After prefix filter:', len(meta_filtered))
else:
    meta_filtered = meta
    print('No prefix filter applied')

meta_filtered = meta_filtered.copy()
meta_filtered['timestamp'] = meta_filtered.apply(parse_timestamp, axis=1)
meta_filtered = meta_filtered.dropna(subset=['timestamp'])
print('After timestamp parse:', len(meta_filtered))

meta_filtered['image_path'] = meta_filtered.apply(find_image_path, axis=1)
print('Example image path:', meta_filtered['image_path'].iloc[0] if len(meta_filtered) else 'N/A')
meta_filtered = meta_filtered[meta_filtered['image_path'].apply(os.path.exists)]
print('After image path exists check:', len(meta_filtered))