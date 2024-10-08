import time
from abc import ABC, abstractmethod

import ddddocr
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
    def _check_html(html: str) -> bool:
        """检查网页内容是否需要人机验证

        :param html: 网页内容
        :return: 是否需要人机验证
        """
        tree = etree.HTML(html)
        total_data = tree.xpath("//h2[@class='total fl']/span/text()")
        return not total_data

    @staticmethod
    def _save_cookie(cookie: str):
        """保存cookie

        :param cookie: cookie字符串
        """
        new_cookie = serialize_cookie(list(cookie))
        cookie_path = get_config("cookie", "cookie_path")
        with open(cookie_path, "w", encoding="utf-8") as f:
            f.write(str(new_cookie))

    @staticmethod
    def _get_verification_code(package: str) -> str:
        """获取验证码

        :param package: 数据包
        :return: 验证码
        """
        base64_code = package.split(" ")[3]
        base64_code = base64_code[:-2]
        code = ddddocr.DdddOcr().classification(base64_code)
        return code

    def do_human_verify(self):
        """人机验证"""
        # 用旧的cookie访问页面
        browser = Chromium()
        tab = browser.latest_tab
        cookie = get_beike_cookie(to_str=True)
        tab.set.cookies(cookie)
        url = get_config("request", "url")
        tab.get(url)
        # 人机验证
        if self._check_html(tab.html):
            tab.listen.start("data:image/jpeg;base64")
            tab.ele("@text()=点击验证").click()
            pic_package = tab.listen.wait()  # 等待并获取图片数据包
            verification_code = self._get_verification_code(str(pic_package))

            # 反复验证直到验证码正确
            status = False
            while not status:
                verification_code = ""
                # 如果验证码不是4位数字，则重新获取验证码
                while len(verification_code) != 4 or not verification_code.isdigit():
                    tab.ele("@class=image-code").click()
                    pic_package = tab.listen.wait()  # 等待并获取一个数据包
                    verification_code = self._get_verification_code(str(pic_package))
                tab.ele("@class=on").input(verification_code)
                time.sleep(3)
                # 保存cookie
                if not self._check_html(tab.html):
                    self._save_cookie(tab.cookies())
                    status = True
                    print("重新获取cookie成功")
        else:
            self._save_cookie(tab.cookies())
        browser.quit
