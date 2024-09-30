import pytest

from src.config import get_config, add_config, delete_config, update_config


@pytest.fixture
def test_config():
    add_config("Test1", "cookie", "123123123123123")
    add_config("Test2", "header", "ndkjahsdakjsndn")
    add_config("Test3", "user", "admin")
    add_config("Test3", "password", "123456")
    add_config("Test4", "database", "data/data.db")
    yield
    delete_config("Test1", "cookie")
    delete_config("Test2", "header")
    delete_config("Test3", "user")
    delete_config("Test3", "password")
    delete_config("Test4", "database")


def test_get_config(test_config):
    cookie = get_config("Test1", "cookie")
    header = get_config("Test2", "header")
    user = get_config("Test3", "user")
    password = get_config("Test3", "password")
    database = get_config("Test4", "database")
    assert cookie == "123123123123123"
    assert header == "ndkjahsdakjsndn"
    assert user == "admin"
    assert password == "123456"
    assert database == "data/data.db"

def test_add_config():
    add_config("Test5", "cookie", "99999999")
    cookie = get_config("Test5", "cookie")
    assert cookie == "99999999"
    delete_config("Test5", "cookie")

def test_update_config(test_config):
    update_config("Test1", "cookie", "11111111")
    update_config("Test2", "header", "22222222")
    update_config("Test3", "user", "9999999")
    update_config("Test3", "password", "88888888")  
    cookie = get_config("Test1", "cookie")
    header = get_config("Test2", "header")
    user = get_config("Test3", "user")
    password = get_config("Test3", "password")
    assert cookie == "11111111"
    assert header == "22222222"
    assert user == "9999999"
    assert password == "88888888"
