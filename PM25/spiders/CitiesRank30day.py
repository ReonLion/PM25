# -*- coding: utf-8 -*-
import scrapy
from PM25.items import *

class Citiesrank30daySpider(scrapy.Spider):
    name = 'CitiesRank30day'
    allowed_domains = ['pm25.com']
    
    def start_requests(self):
        header_dict = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Host":"www.pm25.com",
            "Referer":"http://www.pm25.com/rank/7day.html",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36 OPR/47.0.2631.80",
            "X-Requested-With":"XMLHttpRequest",
        }
        
        yield scrapy.Request(url='http://www.pm25.com/rank/30day.html',
                             callback=self.parse,
                             method='GET',
                             headers=header_dict)

    def parse(self, response):
        sub_select = response.xpath('''//ul[contains(@class, "pj_area_data_details") and contains(@class, "rrank_box")]
        /li[contains(@class, "pj_area_data_item")]''')
        for sub in sub_select:
            item = CitiesRank30dayItem()
            item['ranknum'] = sub.xpath('./span[@class="pjadt_ranknum"]/text()').extract()[0]
            item['quality'] = sub.xpath('./span[@class="pjadt_quality"]/em/text()').extract()[0]
            item['city'] = sub.xpath('./a[@class="pjadt_location"]/text()').extract()[0]
            item['link'] = sub.xpath('./a[@class="pjadt_location"]/@href').extract()[0]
            item['province'] = sub.xpath('./span[@class="pjadt_sheng"]/text()').extract()[0]
            item['aqi'] = sub.xpath('./span[@class="pjadt_aqi"]/text()').extract()[0]
            item['pm25'] = sub.xpath('./span[@class="pjadt_pm25"]/text()').extract()[0]
            item['pm25'] = item['pm25']+sub.xpath('./span[@class="pjadt_pm25"]/em/text()').extract()[0]
            item['link'] = 'http://www.pm25.com' + item['link']
            item['check_time'] = response.xpath('//div[@class="rank_banner_right"]/span/text()').extract()[0]
            yield item
            