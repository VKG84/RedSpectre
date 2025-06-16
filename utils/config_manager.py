import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

DEFAULT_CONFIG = {
    "scan_ports": "",
    "scan_mode": "Complet (-sV -O)",
    "nuclei_threads": "10",
    "nuclei_timeout": "5",
    "nuclei_verbose": False,
    "nuclei_path": "",
    "output_dir": "./rapports",
    "auto_export": False
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)
