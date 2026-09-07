from __future__ import annotations
from pathlib import Path
import yaml


def load_rules(path: str|Path) -> dict:
    with open(path,"r",encoding="utf-8") as f:
        data=yaml.safe_load(f)
    if not isinstance(data,dict) or "rules" not in data:
        raise ValueError("Rules YAML must contain a top-level 'rules' mapping/list")
    return data
