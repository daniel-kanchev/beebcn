import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from beebcn.items import Article
import requests
import json
import re


class beebcnSpider(scrapy.Spider):
    name = 'beebcn'
    start_urls = ['http://www.beeb.com.cn/#/home/banknews']

    def parse(self, response):
        json_response = json.loads(requests.get(
            "http://www.beeb.com.cn/beebPortal/data/content/banknews.json?MmEwMD=5RroZJL4EsQSA_im0lwzRvTmJYy8PJ4cOClXNiNribCHRHjumBO3uBMMxoJzIJ3r62_9HrN9.tr70HIghQ5aKUXz1cuP4ESFycL1xKjK_Na4.JFV_a8PKOxBOF0DcMGoWbpFpqiVpl2aZy2VGwcostDBYt9hUkpu3u7a7ICHNf_K32mxnn0_.wxIMLtrYIf7PM3bZt993kiMI8Nyen.9unNqhUhblx0ILi5cJrPveYNJPVtvuppJobjGdG6nFKcBtQ_nFPjWN0kounYjSEQWn0O.t.BuCKWKbuGZkMNlyziFmT02JgsR0BLc4tfTEvv36").text)
        articles = json_response["articleList"]
        for article in articles:
            item = ItemLoader(Article())
            item.default_output_processor = TakeFirst()

            title = article["title"]
            date = article["createTime"]
            p = re.compile(r'<.*?>')
            content = p.sub('', article["content"])

            item.add_value('title', title)
            item.add_value('date', date)
            item.add_value('content', content)

            yield item.load_item()
