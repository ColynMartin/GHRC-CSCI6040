from __future__ import annotations

import os
import random
from pathlib import Path
from typing import Any, Dict

import numpy as np
import torch
import yaml


def load_yaml(path: str | os.PathLike[str]) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_dir(path: str | os.PathLike[str]) -> Path:
    out = Path(path)
    out.mkdir(parents=True, exist_ok=True)
    return out


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def resolve_device(device_setting: str = "auto") -> str:
    if device_setting != "auto":
        return device_setting
    return "cuda" if torch.cuda.is_available() else "cpu"
