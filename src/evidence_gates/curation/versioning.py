"""Dataset and template version helpers."""

from pathlib import Path

import yaml


def load_dataset_version(config_path: Path) -> dict:
    """Load a dataset version YAML config file."""
    with config_path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        msg = f"Expected mapping in dataset version config: {config_path}"
        raise ValueError(msg)
    return data


def get_default_dataset_version() -> str:
    """Return the default dataset version string from project config."""
    return "v0.1"
