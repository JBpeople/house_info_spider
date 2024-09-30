from abc import ABC, abstractmethod

from DrissionPage import Chromium
from lxml import etree

from src.config import get_config
from src.spider.cookie import get_beike_cookie, serialize_cookie


class HumanVerification(ABC):
    """人机验证抽象类

    :param ABC: 抽象类
    """

    @abstractmethod
    def do_human_verify(self):
        """人机验证"""
        pass


class BeiKeHumanVerification(HumanVerification):
    """贝壳找房人机验证

    :param HumanVerification: 人机验证抽象类
    """

    @staticmethod
    def do_human_verify():
        """人机验证"""
        # 设置cookie
        browser = Chromium()
        tab = browser.latest_tab
        cookie = get_beike_cookie(to_str=True)
        tab.set.cookies(cookie)
        # 访问页面
        url = get_config("request", "url")
        tab.get(url)
        html = tab.html
        # 解析html
        tree = etree.HTML(html)
        total_data = tree.xpath("//h2[@class='total fl']/span/text()")
        if not total_data:  # 如果total_data为空，说明需要人机验证
            input("请输入任意键继续获取cookie...")
        new_cookie = serialize_cookie(list(tab.cookies()))
        cookie_path = get_config("cookie", "cookie_path")
        with open(cookie_path, "w", encoding="utf-8") as f:
            f.write(str(new_cookie))
        browser.quit
