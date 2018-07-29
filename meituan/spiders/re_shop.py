from meituan.spiders.spider import MeituanSpider, ShopSpider

'''

class ZKSpider(MeituanSpider):
    name = 'zk'
    city = '周口'
    start_urls = (
            "http://zk.meituan.com/meishi/",
            )
    base_url = "http://www.meituan.com/meishi/"



class ZKShopSpider(ShopSpider):
    name = 'zk_shop'
    city = '周口'
    citydbname = CITYDBNAME
    start_urls = (
            "http://baidu.com",
            )
    base_url = "http://www.meituan.com/meishi/"




response = None
shop_spider = ZKShopSpider()

shop_spider.parse(response)
'''