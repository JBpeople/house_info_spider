import pytest
from src.spider.page_handler import BeiKePageNumHandler
from src.spider.spider import BeiKeSpider


@pytest.fixture
def test_beike_spider_get_page_url(mocker):
    spider = BeiKeSpider("https://nt.ke.com/ershoufang/rugaoshi/pg1y2/")

    # 模拟 BeiKePageNumHandler.get_page_num() 的返回值
    mocker.patch.object(BeiKePageNumHandler, "get_page_num", return_value=5)

    # 获取生成器对象
    page_urls = spider.get_page_url()
    assert len(page_urls) == 5

    # 验证生成的URL格式是否正确
    for i, url in enumerate(spider.get_page_url(), start=1):
        assert url == f"https://nt.ke.com/ershoufang/rugaoshi/pg{i}y2/"

# spider = BeiKeSpider("https://nt.ke.com/ershoufang/rugaoshi/pg1y2/")
# print(spider.get_page_url())