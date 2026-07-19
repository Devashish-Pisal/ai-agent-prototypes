from pathlib import Path

# PATH CONFIG
# Folders
PROJECT_ROOT = Path(__file__).parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
PROMPTS_DIR = PROJECT_ROOT / "prompts"
SRC_DIR = PROJECT_ROOT / "src"
STORAGE_DIR = PROJECT_ROOT / "storage"

# Files
INVOICE_CLASSIFICATION_PROMPT_FILE = PROMPTS_DIR / "invoice_classifier.txt"
CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "token.json"
SECRETS_FILE = PROJECT_ROOT / ".env"