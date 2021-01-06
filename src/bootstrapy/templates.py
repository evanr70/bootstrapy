import bootstrapy
from bootstrapy import body_tags, head_tags
from bootstrapy.config import get_config
from bootstrapy.nav import create_nav
from bs4 import BeautifulSoup, Doctype


def apply_config(soup, root_dir=""):
    config = get_config(root_dir)
    title = soup.new_tag("title")
    soup.head.append(title)
    title.string = config["name"]
    for location in soup.find_all(class_="nav-location-text"):
        location.string = config["location-or-company"]
    for job in soup.find_all(class_="nav-job-text"):
        job.string = config["occupation"]
    for email in soup.find_all(class_="nav-email-link"):
        email.attrs["href"] = "".join(["mailto:", config["email"]])
    for github in soup.find_all(class_="nav-gh"):
        github.attrs["href"] = "".join(["http://github.com/", config["github"]])
    for twitter in soup.find_all(class_="nav-twitter"):
        twitter.attrs["href"] = "".join(["http://twitter.com/", config["twitter"]])


def delete_content_id(soup):
    content_tag = soup.find(id="content")
    if content_tag is not None:
        del content_tag.attrs["id"]


def bare_bones(site_name="", **kwargs):
    soup = BeautifulSoup("", "html.parser")
    soup.append(Doctype("html"))
    html = soup.new_tag("html", attrs={"lang": "en"})
    soup.append(html)
    html.append(soup.new_tag("head"))
    html.append(soup.new_tag("body", id="content"))
    apply_config(soup, site_name)
    return soup


def bootstrap(site_name="", **kwargs):
    soup = bare_bones(site_name)
    head = head_tags.bootstrap()
    for tag in head:
        soup.head.append(tag)
    soup.body.append(body_tags.bootstrap_script)
    delete_content_id(soup)
    soup.body.append(soup.new_tag("div", id="content"))
    apply_config(soup, site_name)
    return soup


def with_fonts(site_name="", **kwargs):
    soup = bootstrap(site_name)
    head = head_tags.fonts()
    for tag in head:
        soup.head.append(tag)
    apply_config(soup, site_name)
    return soup


def sidebar(site_name="", **kwargs):
    with (bootstrapy.resources / "sidebars.html").open() as f:
        sidebar_soup = BeautifulSoup(f.read(), "html.parser")
    return sidebar_soup


def nav_only(site_name="", **kwargs):
    soup = bootstrap(site_name)
    head = head_tags.fonts()
    for tag in head:
        soup.head.append(tag)
    soup.body.append(create_nav(site_name))
    delete_content_id(soup)
    soup.body.append(soup.new_tag("div", id="content"))
    apply_config(soup, site_name)
    return soup


def frame(site_name="", **kwargs):
    soup = with_fonts(site_name)
    soup.body.append(create_nav(site_name))
    soup.body.append(sidebar(site_name))
    delete_content_id(soup)
    main_tag = body_tags.main_tag
    content_tag = main_tag.find("div")
    content_tag.attrs["id"] = "content"
    main_tag.append(content_tag)
    soup.body.append(main_tag)
    apply_config(soup, site_name)
    return soup


def get_templates():
    return {
        "bare_bones": bare_bones,
        "bootstrap": bootstrap,
        "with_fonts": with_fonts,
        "nav_only": nav_only,
        "frame": frame,
    }
