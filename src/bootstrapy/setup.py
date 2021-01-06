import shutil
from pathlib import Path

import bootstrapy
import requests
from bootstrapy import templates
from bootstrapy.config import config_file

directories = [
    "pages",
    "_pages",
    "posts",
    "_posts",
    "assets",
    "css",
    "fonts",
    "templates",
    "config",
]


def create_structure(site_name):
    root = Path(site_name)
    root.mkdir(parents=True, exist_ok=True)
    for directory in directories:
        (root / directory).mkdir()


def clean_output(site_name=""):
    check_structure(site_name)
    root = Path(site_name)
    pages = list((root / "pages").glob("*.html"))
    posts = list((root / "posts").glob("*.html"))
    all_outputs = pages + posts

    for output in all_outputs:
        print(f"Deleting {output}.")
        output.unlink()
    print(f"Cleaned {root}.")


def check_structure(site_name):
    root = Path(site_name)
    for directory in directories:
        path = root / directory
        if not path.exists():
            raise FileNotFoundError(f"The directory '{path}' was not found.")
        if not path.is_dir():
            raise NotADirectoryError(f"{path} is not a directory.")
    print("All directories found.")


def get_resources(root_name):
    social_circles = "http://janhuenermann.github.io/social-circles/"

    social_css = "css/social-circles.css"
    social_font = "fonts/socialfont"
    font_extensions = [".woff", ".eot", ".svg", ".ttf"]
    social_fonts = ["".join([social_font, extension]) for extension in font_extensions]
    paths = [social_css] + social_fonts

    root_path = Path(root_name)

    for path in paths:
        file = root_path / path
        url = "".join([social_circles, path])
        print(f"Downloading: {url} ---> {file}")
        content = requests.get(url).content
        with file.open("wb") as f:
            f.write(content)

    pygments_css = (
        "https://raw.githubusercontent.com/richleland/pygments-css/master/default.css"
    )
    file = root_path / "css" / "pygments.css"

    print(f"Downloading: {pygments_css} ---> {file}")
    content = requests.get(pygments_css).content
    with file.open("wb") as f:
        f.write(content)

    print("Moving main.css.")
    main_css = bootstrapy.resources / "main.css"
    shutil.copy(str(main_css), str(root_path / "css"))


def generate_templates(root_name):
    template_dict = templates.get_templates()
    for name, template in template_dict.items():
        template_path = (Path(root_name) / "templates" / name).with_suffix(".html")
        print(f"Creating template '{name}' at {template_path}")
        template_soup = template(site_name=root_name)
        with template_path.open("w") as f:
            f.write(template_soup.prettify())


def init(site_name=""):
    print("Creating site structure...")
    create_structure(site_name)
    print("Downloading and copying resources...")
    get_resources(site_name)
    print("Creating config file...")
    config_file(site_name)
    print("Generating templates...")
    generate_templates(site_name)
    print("Finished.")


if __name__ == "__main__":
    init()
