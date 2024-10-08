import os
import re
from typing import List

from src.config import get_config


def serialize_cookie(cookie: List[dict]) -> str:
    """序列化cookie

    :param cookie: cookie列表
    :return: cookie字符串
    """
    cookie_str = ""
    for item in cookie:
        cookie_str += f"{item['name']}={item['value']}; "
    return cookie_str


def deserialize_cookie(cookie_string: str) -> dict:
    """
    将cookie字符串反序列化为字典

    :param cookie_string: 原始cookie字符串
    :return: 序列化后的cookie字典
    """
    cookie_dict = {}
    for item in cookie_string.split("; "):
        if "=" in item:
            key, value = item.split("=", 1)
            cookie_dict[key] = value.strip()
    return cookie_dict


def add_beike_domain(cookie: dict) -> dict:
    """添加贝壳域名

    :param cookie: 原始cookie字典
    :return: 添加域名后的cookie字典
    """
    url = get_config("request", "url")
    domain = re.findall(r"([a-zA-Z.]+ke.com+/[a-zA-Z]+/[a-zA-Z]+/)", url)[0]
    if not cookie.get("domain"):
        cookie["domain"] = domain
    return cookie


def get_beike_cookie(to_str: bool = False) -> str | dict:
    """获取cookie

    :param cookie_path: cookie文件路径
    :return: cookie字典或者cookie字符串
    """
    cookie_path = get_config("cookie", "cookie_path")
    if not os.path.exists(cookie_path):
        with open(cookie_path, "w") as f:
            f.write("")
    with open(cookie_path, "r") as f:
        cookie_string = f.read().strip()
    if to_str:  # 返回字符串，适配DrissionPage的cookie设置
        domain_dict = add_beike_domain({})
        cookie_string += f" domain={domain_dict['domain']};"
        return cookie_string
    else:  # 返回字典，适配requests的cookie设置
        cookie_dict = deserialize_cookie(cookie_string)
        full_cookie_dict = add_beike_domain(cookie_dict)
        return full_cookie_dict
