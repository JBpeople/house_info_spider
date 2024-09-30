import pytest

from src.database.db import add_house_info, del_house_info, query_house_info, update_house_info
from src.database.model import HouseInfo, get_session


@pytest.fixture
def make_house_info_data():
    house_info_1 = HouseInfo(
        key=101163719061,
        title="1995年电梯房，明厨明卫 高楼层 采光视野好",
        location="三丰里小区",
        total_floor=6,
        at_floor="高楼层",
        year=2024,
        layout="三室一厅",
        area=110,
        direction="南北",
        follower=100,
        upload_time="六月前",
        total_price=1000000,
        unit_price=9090,
    )
    house_info_2 = HouseInfo(
        key=101126719061,
        title="宣武门外东大街 2室0厅 南 北",
        location="宣武门外东大街",
        total_floor=25,
        at_floor="中楼层",
        year=2023,
        layout="二室一厅",
        area=120,
        direction="东",
        follower=100,
        upload_time="一月前",
        total_price=1020000,
        unit_price=8500,
    )
    house_info_3 = HouseInfo(
        key=101126716121,
        title="富卓苑 2室1厅 南 北",
        location="富卓苑",
        total_floor=10,
        at_floor="中楼层",
        year=2021,
        layout="四室一厅",
        area=120,
        direction="东",
        follower=100,
        upload_time="一月前",
        total_price=100000,
        unit_price=8333,
    )
    add_house_info(house_info_1)
    add_house_info(house_info_2)
    add_house_info(house_info_3)
    yield
    with get_session() as session:
        session.query(HouseInfo).filter(HouseInfo.key == 101163719061).delete()
        session.query(HouseInfo).filter(HouseInfo.key == 101126719061).delete()
        session.query(HouseInfo).filter(HouseInfo.key == 101126716121).delete()


def test_add_house_info():
    house_info = HouseInfo(
        key=1,
        title="test",
        location="test",
        total_floor=6,
        at_floor="高楼层",
        year=2024,
        layout="三室一厅",
        area=110,
        direction="南北",
        follower=100,
        upload_time="六月前",
        total_price=1000000,
        unit_price=9090,
    )
    assert query_house_info(key=1) is not None
    with get_session() as session:
        session.query(HouseInfo).filter(HouseInfo.key == 1).delete()


@pytest.mark.parametrize(
    "input, output",
    [
        (101126716121, "富卓苑"),
        (101163719061, "三丰里小区"),
        (101126719061, "宣武门外东大街"),
    ],
)
def test_query_house_info(make_house_info_data, input, output):
    assert query_house_info(key=input)[0].location == output


@pytest.mark.parametrize(
    "input, output",
    [
        (101126716121, 1000),
        (101163719061, 2000),
        (101126719061, 3000),
    ],
)
def test_update_house_info(make_house_info_data, input, output):
    update_house_info(key=input, follower=output)
    assert query_house_info(key=input)[0].follower == output


@pytest.mark.parametrize(
    "input",
    [
        (101126716121),
        (101163719061),
        (101126719061),
    ],
)
def test_del_house_info(make_house_info_data, input):
    del_house_info(key=input)
    house_info = query_house_info(key=input)
    assert house_info[0].deleted_at is not None
