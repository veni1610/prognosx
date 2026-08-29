import os

# ---- Paths (EDIT THESE to match your actual MIMIC-CXR file locations) ----
MIMIC_CXR_IMAGE_ROOT = "data/raw"
MIMIC_CXR_METADATA_CSV = "data/raw/mimic-cxr-2.0.0-metadata.csv"
MIMIC_CXR_CHEXPERT_CSV = "data/raw/mimic-cxr-2.0.0-metadata.csv"

OUTPUT_DIR = "./outputs"
EMBEDDINGS_DIR = os.path.join(OUTPUT_DIR, "embeddings")
SEQUENCES_DIR = os.path.join(OUTPUT_DIR, "sequences")
CHECKPOINT_DIR = os.path.join(OUTPUT_DIR, "models")
RESULTS_DIR = os.path.join(OUTPUT_DIR, "results")

for d in [OUTPUT_DIR, EMBEDDINGS_DIR, SEQUENCES_DIR, CHECKPOINT_DIR, RESULTS_DIR]:
    os.makedirs(d, exist_ok=True)

# ---- CheXpert findings tracked (matches base paper's 10 classes) ----
CHEXPERT_CLASSES = [
    "No Finding", "Cardiomegaly", "Lung Opacity", "Edema",
    "Consolidation", "Pneumonia", "Atelectasis", "Pneumothorax",
    "Pleural Effusion", "Pleural Other"
]

# ---- Vision encoder ----
# NOTE: The base paper (CXR-TFT) uses BioCLIP. We use torchxrayvision's
# DenseNet instead: it is trained directly on chest X-ray datasets
# (including MIMIC-CXR), unlike BioCLIP which is a general biological
# tree-of-life model repurposed for radiology. It also preserves spatial
# feature maps needed for our planned Grad-CAM module, and runs fully
# locally without external API dependencies.
IMAGE_EMBED_DIM = 1024  # torchxrayvision densenet121 feature dim

# ---- Clinical features ----
# PLACEHOLDER until MIMIC-IV is available (expected Aug 31).
CLINICAL_FEATURE_DIM = 20

FUSION_INPUT_DIM = IMAGE_EMBED_DIM + CLINICAL_FEATURE_DIM

# ---- Training ----
BATCH_SIZE = 4
LEARNING_RATE = 5e-4
WEIGHT_DECAY = 0.01
NUM_EPOCHS = 100
EARLY_STOP_PATIENCE = 10
DROPOUT = 0.1
ALPHA = 0.5
D_MODEL = 256
N_HEADS = 4
N_LAYERS = 2
MAX_SEQ_LEN = 48