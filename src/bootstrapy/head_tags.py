from bs4 import BeautifulSoup

_soup = BeautifulSoup("", "html.parser")

charset = _soup.new_tag("meta", attrs={"charset": "utf-8"})
viewport = _soup.new_tag(
    "meta", attrs={"name": "viewport", "content": "width=device-width, initial-scale=1"}
)

bootstrap_css = _soup.new_tag(
    "link",
    attrs={
        "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/"
        "dist/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9"
        "wjKHr8RbDVddVHyTfAAsrekwKmP1",
        "crossorigin": "anonymous",
    },
)

font_awesome_css = _soup.new_tag(
    "link",
    attrs={
        "href": "https://stackpath.bootstrapcdn.com/"
        "font-awesome/4.7.0/css/font-awesome.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+"
        "QkPxCAFlNEevoEH3Sl0sibVcOQVnN",
        "crossorigin": "anonymous",
    },
)

social_buttons_css = _soup.new_tag(
    "link", attrs={"href": "../css/social-circles.css", "rel": "stylesheet"},
)

google_fonts = _soup.new_tag(
    "link", attrs={"href": "https://fonts.gstatic.com", "rel": "preconnect"}
)

roboto_mono = _soup.new_tag(
    "link",
    attrs={
        "href": "https://fonts.googleapis.com/"
        "css2?family=Roboto+Mono:wght@600&display=swap",
        "rel": "stylesheet",
    },
)

main_css = _soup.new_tag("link", attrs={"href": "../css/main.css", "rel": "stylesheet"})


def fonts():
    return [
        font_awesome_css,
        social_buttons_css,
        google_fonts,
        roboto_mono,
        main_css,
    ]


def default():
    return [charset, viewport, bootstrap_css, main_css] + fonts()


def bootstrap():
    return [
        charset,
        viewport,
        bootstrap_css,
        font_awesome_css,
        main_css,
    ]


del _soup
