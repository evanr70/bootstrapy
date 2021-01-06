"""bootstrapy.py

Usage:
    bootstrapy.py init
    bootstrapy.py init <directory>
    bootstrapy.py create
    bootstrapy.py create <directory>
    bootstrapy.py reindex
    bootstrapy.py reindex <directory>

"""

from bootstrapy import __version__, pages, setup, validation
from docopt import docopt

__author__ = "Evan Roberts"
__copyright__ = "Evan Roberts"
__license__ = "mit"


def init(directory):
    setup.init(directory)


def create(directory):
    pages.get_all(directory)
    validation.validate_hrefs(directory)
    pages.list_posts(directory)


def reindex(directory):
    pages.list_posts(directory)


def run():
    args = docopt(__doc__, version=__version__)
    if args["init"]:
        init(args["<directory>"] or "")
    if args["create"]:
        create(args["<directory>"] or "")
    if args["reindex"]:
        reindex(args["<directory>"] or "")


if __name__ == "__main__":
    run()
