import datetime
from typing import List

from src.database.model import HouseInfo, get_session


def add_house_info(house_info: HouseInfo):
    """添加房产信息

    :param house_info: 房产信息
    """
    with get_session() as session:
        session.add(house_info)


def query_house_info(**kwargs) -> List[HouseInfo]:
    """house_info: 查询数据

    :return: 房产信息列表
    """
    q = []
    for v in kwargs.values():
        q.append(HouseInfo.key == v)
    with get_session() as session:
        if q:
            datas = session.query(HouseInfo).filter(*q).all()
        else:
            datas = session.query(HouseInfo).all()
        return datas


def update_house_info(key: int, **kwargs):
    """更新房产信息

    :param key: 房产信息key
    """
    with get_session() as session:
        session.query(HouseInfo).filter(HouseInfo.key == key).update(kwargs)


def del_house_info(key: int):
    """删除房产信息

    :param key: 房产信息key
    """
    with get_session() as session:
        house_info = session.query(HouseInfo).filter(HouseInfo.key == key).first()
        update_house_info(key=house_info.key, deleted_at=datetime.datetime.now())
