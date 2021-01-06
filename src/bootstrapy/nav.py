from bootstrapy.config import get_config
from bs4 import BeautifulSoup


def nav_item(page_name, file_name=None):
    if file_name is None:
        file_name = ".".join([page_name.lower().replace(" ", "-"), "html"])
    item_soup = BeautifulSoup("", "html.parser")
    li = item_soup.new_tag("li", attrs={"class": "nav-item"})
    anchor = item_soup.new_tag(
        "a",
        attrs={
            "class": "btn text-white",
            "href": f"../pages/{file_name}",
            "role": "button",
        },
    )
    anchor.string = page_name
    item_soup.append(li)
    li.append(anchor)

    return item_soup


def create_nav(site_name=""):
    config = get_config(site_name)
    page_names = config["nav-items"]
    nav_soup = BeautifulSoup("", "html.parser")
    nav_tag = nav_soup.new_tag(
        "nav", id="nav-top", attrs={"class": "navbar navbar-dark bg-dark navbar-expand"}
    )
    container = nav_soup.new_tag(
        "div", attrs={"class": "container-fluid", "id": "nav-insert-point"}
    )
    brand = nav_soup.new_tag(
        "a", attrs={"class": "navbar-brand", "href": "../pages/index.html"}
    )
    brand.string = config["name"]
    ul = nav_soup.new_tag("ul", attrs={"class": "nav navbar-nav ml-auto"})

    nav_soup.append(nav_tag)
    nav_tag.append(container)
    container.append(brand)
    container.append(ul)

    for page in page_names:
        ul.append(nav_item(page))

    return nav_soup
