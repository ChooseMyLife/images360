from scrapy import Spider, Request
from urllib.parse import urlencode
import scrapy
from images360.items import ImagesItem
import json


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']

    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = ImagesItem()
            item['id'] = image.get('id')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('title')
            item['thumb'] = image.get('qhimg_thumb')
            yield item

    def start_requests(self):
        data = {'ch': 'photography', 'listtype': 'new'}
        baseurl = 'https://images.so.com/zjl?'
        for page in range(1, self.settings.get('MAX_PAGE')+1):
            data['sn'] = page*30
            params = urlencode(data)
            url = baseurl + params
            yield Request(url, self.parse)
