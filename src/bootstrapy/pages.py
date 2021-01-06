import re
from copy import copy
from pathlib import Path

from bootstrapy.templates import get_templates
from bs4 import BeautifulSoup, Comment, Tag
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer


"""       <ul>
        <li>
         <a class="text-decoration-none" href="/posts/altplotlib_example.html">
          altplotlib example
         </a>
        </li>
        <li>
         <a class="text-decoration-none" href="/posts/latex_to_png.html">
          latex to png
         </a>
        </li>
       </ul>
"""


def post_list_index(names, hrefs):
    post_soup = BeautifulSoup("", "html.parser")
    ul = post_soup.new_tag("ul", id="post-list-index")
    post_soup.append(ul)

    for name, href in zip(names, hrefs):
        li = post_soup.new_tag("li")
        a = post_soup.new_tag(
            "a", attrs={"class": "text-decoration-none", "href": href}
        )
        a.string = name
        li.append(a)
        ul.append(li)
    return ul


def get_template_name(soup):
    pattern = re.compile(r"template:\s*(.*?)$")
    comments = soup.find_all(text=lambda e: isinstance(e, Comment))
    name = ""
    for comment in comments:
        match = pattern.search(comment)
        if match is not None:
            name = match.group(1)
            comment.extract()
            break
    return name or "frame"


def list_posts(root_path=""):
    post_index = Path(root_path) / "pages" / "posts.html"
    index_soup = BeautifulSoup(post_index.read_text(), "html.parser")

    content_child = list(
        tag for tag in index_soup.find(id="content").children if isinstance(tag, Tag)
    )[-1]

    names = []
    hrefs = []
    posts = list((Path(root_path) / "posts").glob("*.html"))
    for post in posts:
        with post.open() as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        title_comment = soup.find(
            string=lambda text: isinstance(text, Comment) and ("title:" in text)
        )
        if title_comment is None:
            # title = get_config(root_path)["name"]
            title = str(post.name).replace(".html", "").replace("_", " ")
        else:
            title = re.match(r"title:\s*(.*?)$", title_comment).group(1)

        title_tag = soup.find("title")
        if title_tag is None:
            title_tag = soup.new_tag("title")
            soup.head.append(title_tag)
        title_tag.string = title

        with post.open("w") as f:
            f.write(soup.prettify())

        names.append(title)
        hrefs.append(f"../posts/{post.name}")

    previous_list = index_soup.find(id="post-list-index")
    if previous_list is not None:
        previous_list.extract()

    index = post_list_index(names, hrefs)
    content_child.append(index)

    print("Indexing posts...")
    post_index.write_text(index_soup.prettify())


def get_pages(root_path=""):
    fill_templates(root_path, "pages")


def get_posts(root_path=""):
    fill_templates(root_path, "posts")


def fill_templates(root_path, directory):
    page_inputs = list((Path(root_path) / f"_{directory}").glob("*.html"))
    for page_input in page_inputs:
        page_output = Path(root_path) / f"{directory}" / page_input.name
        print(f"Constructing {page_input} ---> {page_output}")
        with page_input.open() as f:
            page_data = BeautifulSoup(f.read(), "html.parser")
        template_name = get_template_name(page_data)
        working_copy = copy(get_templates()[template_name](site_name=root_path))
        working_copy.find(id="content").append(page_data)
        add_vega_plots(working_copy, root_path)
        highlight_html(working_copy)
        with page_output.open("w") as f:
            f.write(working_copy.prettify())


def get_all(root_path=""):
    get_posts(root_path)
    get_pages(root_path)


def add_vega_head(soup):
    sources = [
        "https://cdn.jsdelivr.net/npm//vega@5",
        "https://cdn.jsdelivr.net/npm//vega-lite@4.8.1",
        "https://cdn.jsdelivr.net/npm//vega-embed@6",
    ]

    style = soup.new_tag("style")
    style.string = ".error {color: red;}"
    soup.head.append(style)

    for source in sources:
        soup.head.append(
            soup.new_tag("script", attrs={"type": "text/javascript", "src": source})
        )


def add_vega_plots(soup, root_path=""):
    asset_directory = Path(root_path) / "assets"

    vega_comments = soup.find_all(
        string=lambda text: isinstance(text, Comment) and ("vega:" in text)
    )

    vega_added = False
    vega_pattern = re.compile("vega: (.*?)$")
    for comment in vega_comments:
        if not vega_added:
            add_vega_head(soup)
            vega_added = True
        vega_file_name = vega_pattern.search(comment.string).group(1)
        vega_file = (asset_directory / vega_file_name).with_suffix(".html")

        print(f"Including Vega: {vega_file}")
        with open(vega_file) as f:
            vega_soup = BeautifulSoup(f.read(), "html.parser")
        vega_body = vega_soup.body
        vega_body.name = "div"

        comment.replace_with(vega_body)


def add_pygments_css(soup):
    tag = soup.new_tag(
        "link", attrs={"href": "../css/pygments.css", "rel": "stylesheet"},
    )
    soup.head.append(tag)


def highlight_html(soup):
    css_added = False

    for item in soup.find_all("code", lang="python"):
        if not css_added:
            add_pygments_css(soup)
        code_text = highlight(item.text, PythonLexer(), HtmlFormatter(wrapcode=True))
        s2 = BeautifulSoup(code_text, "html.parser")
        item.parent.replace_with(s2)
