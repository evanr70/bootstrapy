from bs4 import BeautifulSoup

_soup = BeautifulSoup("", "html.parser")

bootstrap_script = _soup.new_tag(
    "script",
    attrs={
        "src": "https://cdn.jsdelivr.net/npm/"
        "bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js",
        "integrity": "sha384-"
        "ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW",
        "crossorigin": "anonymous",
    },
)

main_tag = _soup.new_tag("div", attrs={"class": "col-sm-12 main"})
container_tag = _soup.new_tag("div", attrs={"class": "container pt-3"})
main_tag.append(container_tag)

del _soup
