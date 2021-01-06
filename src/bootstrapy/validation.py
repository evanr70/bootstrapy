import re
from pathlib import Path

import validators
from bootstrapy import setup
from bs4 import BeautifulSoup


def mailto_validator(href):
    mailto = re.match("mailto:(.*?)$", href)
    if mailto is not None:
        href = mailto.group(1)
    return validators.email(href)


def file_validator(href, root_dir="", file_path=""):
    if href.startswith("/"):
        path = Path(root_dir) / href
    elif href.startswith("../"):
        path = Path(file_path).parent.parent / href.replace("../", "")
    else:
        return False
    return path.exists()


def validate(hrefs, file_path, root_dir=""):
    valid_urls = [validators.url(href) for href in hrefs]
    valid_emails = [mailto_validator(href) for href in hrefs]
    valid_files = [
        file_validator(href, file_path=file_path, root_dir=root_dir) for href in hrefs
    ]

    valid_href = [
        bool(vu) | bool(ve) | bool(vf)
        for vu, ve, vf in zip(valid_urls, valid_emails, valid_files)
    ]
    return valid_href


def validate_hrefs(root_name=""):
    setup.check_structure(root_name)
    directories = sum(
        [list((Path(root_name) / d).glob("*")) for d in ["pages", "posts"]], start=[]
    )

    for file in directories:

        with file.open() as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        urls = [tag.attrs["href"] for tag in soup.find_all(href=True)]

        valid_href = validate(urls, file, root_name)

        if all(valid_href):
            print(f"All links validated in '{file}'")
        else:
            for href, valid in zip(urls, valid_href):
                if not valid:
                    print(f"'{href}' is not a valid file, email or url.")
