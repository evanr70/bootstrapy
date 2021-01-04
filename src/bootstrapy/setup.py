from pathlib import Path


def create_structure(site_name):
    root = Path(site_name)
    directories = [
        "pages",
        "_pages",
        "posts",
        "_posts",
        "assets",
        "css",
        "fonts",
        "templates",
    ]
    root.mkdir(parents=True, exist_ok=True)
    for directory in directories:
        (root / directory).mkdir()
