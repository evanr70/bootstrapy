from pathlib import Path

import yaml


def get_config(root_name=""):
    config_path = Path(root_name) / "config" / "config.yaml"
    with config_path.open("r") as f:
        return yaml.load(f, Loader=yaml.Loader)


def config_file(root_name):
    config_path = Path(root_name) / "config" / "config.yaml"

    default_config = {
        "name": "Your Name",
        "location-or-company": "Your Location",
        "occupation": "Occupation",
        "email": "example@example.com",
        "github": "username",
        "twitter": "username",
        "nav-items": ["Posts", "Research", "Projects"],
    }

    with config_path.open("w") as f:
        yaml.dump(default_config, f)
