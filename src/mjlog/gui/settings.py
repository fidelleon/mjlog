"""GUI settings: Load and save application state."""

import json
from pathlib import Path


def get_settings_file() -> Path:
    """Get mjlog.ini path (in project root)."""
    repo_root = Path(__file__).parent.parent.parent.parent
    return repo_root / "mjlog.ini"


def load_window_state(window_name: str) -> dict:
    """Load saved window state from mjlog.ini."""
    settings_file = get_settings_file()
    if not settings_file.exists():
        return {}

    try:
        with open(settings_file, "r") as f:
            data = json.load(f)
        return data.get(window_name, {})
    except (json.JSONDecodeError, IOError):
        return {}


def save_window_state(window_name: str, state: dict) -> None:
    """Save window state to mjlog.ini."""
    settings_file = get_settings_file()

    # Load existing data
    try:
        if settings_file.exists():
            with open(settings_file, "r") as f:
                data = json.load(f)
        else:
            data = {}
    except (json.JSONDecodeError, IOError):
        data = {}

    # Update window state
    data[window_name] = state

    # Write back
    with open(settings_file, "w") as f:
        json.dump(data, f, indent=2)
