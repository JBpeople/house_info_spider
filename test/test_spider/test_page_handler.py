import pytest

from src.spider.page_handler import BeiKePageHandler, BeiKePageNumHandler
from src.spider.webpage import LocoalWebPage


@pytest.mark.parametrize(
    "input, output",
    [
        ("test/resource/test_html_1.html", 30),
        ("test/resource/test_html_2.html", 25),
        ("test/resource/test_html_3.html", 30),
        ("test/resource/test_html_4.html", 30),
    ],
)
def test_beike_parse_html(input, output):
    webpage = LocoalWebPage(input)
    html = webpage.get_html()
    page_handler = BeiKePageHandler(html)
    html_data = page_handler._parse_html()
    for value in html_data.values():
        assert len(value) == output


@pytest.mark.parametrize(
    "input, output",
    [
        ("test/resource/test_html_1.html", 30),
        ("test/resource/test_html_2.html", 25),
        ("test/resource/test_html_3.html", 30),
        ("test/resource/test_html_4.html", 30),
    ],
)
def test_beike_parse_data(input, output):
    webpage = LocoalWebPage(input)
    html = webpage.get_html()
    page_handler = BeiKePageHandler(html)
    data = page_handler.parse_data()
    for value in data.values():
        assert len(value) == output

@pytest.mark.parametrize(
    "input, output",
    [
        ("test/resource/test_html_1.html", 28),
        ("test/resource/test_html_2.html", 28),
        ("test/resource/test_html_3.html", 28),
        ("test/resource/test_html_4.html", 28),
    ],
)
def test_beike_get_page_num(input, output):
    webpage = LocoalWebPage(input)
    html = webpage.get_html()
    page_handler = BeiKePageNumHandler(html)
    page_num = page_handler.get_page_num()
    assert page_num == output
