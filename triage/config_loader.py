"""
Loads and validates triage_config.yml.
Previously the config file existed but was never read — this fixes that.
"""
import os
import yaml
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config" / "triage_config.yml"


def load_config(path: Path | None = None) -> dict:
    """
    Loads the triage configuration from YAML.
    Falls back to safe defaults if the file is missing or malformed.
    """
    config_path = path or DEFAULT_CONFIG_PATH

    if not config_path.exists():
        logger.warning("Config file not found at %s — using defaults.", config_path)
        return _default_config()

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        logger.info("Config loaded from %s", config_path)
        return config
    except yaml.YAMLError as e:
        logger.error("Failed to parse config file: %s — using defaults.", e)
        return _default_config()


def _default_config() -> dict:
    return {
        "ai_model": os.getenv("AI_MODEL", "gpt-4o-mini"),
        "story_points": [1, 2, 3, 5, 8, 13],
        "labels": {
            "bug": "d73a4a", "feature": "0075ca", "documentation": "0052cc",
            "question": "d876e3", "security": "e4e669",
        },
        "team": [],
    }


def get_label_colors(config: dict) -> dict:
    return config.get("labels", _default_config()["labels"])


def get_ai_model(config: dict) -> str:
    return config.get("ai_model", os.getenv("AI_MODEL", "gpt-4o-mini"))


def get_team(config: dict) -> list[dict]:
    return config.get("team", [])
