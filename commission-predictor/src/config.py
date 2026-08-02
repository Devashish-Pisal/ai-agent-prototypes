from pathlib import Path


# Folder Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SRC_DIR = PROJECT_ROOT / "src"

# File Paths
DATASET_FILE_PATH = DATA_DIR / "data.xlsx"
DATASET_INFO_FILE_PATH = DATA_DIR / "info.xlsx"
PROCESSED_DATA = DATA_DIR / "processed_data.xlsx"