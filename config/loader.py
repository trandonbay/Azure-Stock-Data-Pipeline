import json
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent

def load_config(name: str):
    path = CONFIG_DIR / f"{name}.json"
    with open(path) as f:
        return json.load(f)