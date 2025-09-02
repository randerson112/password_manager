import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
USER_CONFIG_PATH = ROOT_DIR / "config.json"

DEFAULT_CONFIG = {
    "vaults_directory": str(ROOT_DIR) + "/.vaults"
}

# Load configs from file or default configs
def load_config():

    # Create a local config file if it does not exist
    if not os.path.exists(USER_CONFIG_PATH):
        USER_CONFIG_PATH.write_text(json.dumps(DEFAULT_CONFIG, indent=4))
        return DEFAULT_CONFIG
    
    # Retrieve configs from local config file
    with open(USER_CONFIG_PATH, "r") as f:
        return json.load(f)

# Get the vaults directory from config
def get_vaults_directory():
    config = load_config()
    return config.get("vaults_directory")