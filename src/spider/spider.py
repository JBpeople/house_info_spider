import re
from abc import ABC, abstractmethod

from src.err import UrlNotCompleteError
from src.spider.page_handler import BeiKePageHandler, BeiKePageNumHandler
from src.spider.webpage import BeikeWebPage


class Spider(ABC):
    """爬虫抽象类"""

    @abstractmethod
    def get_page_url(self) -> list:
        """获取网页页数

        :return: 网页页数网址
        """
        pass

    @abstractmethod
    def get_page_data(self, url: str) -> dict:
        """获取网页数据

        :param url: 网页链接
        :return: 网页数据
        """
        pass


class BeiKeSpider(Spider):
    """贝壳爬虫"""

    def __init__(self, url: str):
        """初始化贝壳房产爬虫

        :param url: 贝壳网页链接
        """
        self.url = url

    def get_page_url(self) -> list:
        """获取贝壳网页页数

        :return: 贝壳网页页数网址
        """
        # 检查url是否完整
        if "pg" not in self.url:
            raise UrlNotCompleteError("url缺少页数标记")
        # 获取网页内容
        webpage = BeikeWebPage(self.url)
        html = webpage.get_html()
        # 获取网页页数
        page_handler = BeiKePageNumHandler(html)
        page_num = page_handler.get_page_num()
        # 拼接网页网址
        page_pattern = re.compile(r"pg(\d+)")
        result = []
        for i in range(1, page_num + 1):
            new_url = re.sub(page_pattern, f"pg{i}", self.url)
            result.append(new_url)
        return result

    @staticmethod
    def get_page_data(url: str) -> dict:
        """获取贝壳网页数据

        :param url: 贝壳网页链接
        :return: 贝壳网页数据
        """
        webpage = BeikeWebPage(url)
        html = webpage.get_html()
        page_handler = BeiKePageHandler(html)
        data = page_handler.parse_data()
        return data
