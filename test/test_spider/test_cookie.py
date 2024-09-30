import pytest
from src.spider.cookie import get_beike_cookie, deserialize_cookie

def test_serialize_cookie():
    cookie = deserialize_cookie("user=admin; password=123456")
    assert cookie == {"user": "admin", "password": "123456"}

@pytest.fixture
def test_get_beike_cookie(mocker):
    mocker.patch("src.spider.cookie.get_config", return_value="user=admin; password=123456")
    cookie = get_beike_cookie()
    assert cookie == {"user": "admin", "password": "123456"}
    mocker.patch("src.spider.cookie.get_config", return_value="[{'user': 'admin', 'password': '123456'}]")
    cookie = get_beike_cookie()
    assert cookie == [{"user": "admin", "password": "123456"}]
