# -*- coding: utf-8 -*-
import scrapy
from PM25.items import *
import re

class CitiesrankSpider(scrapy.Spider):
    name = 'CitiesRank'
    allowed_domains = ['pm25.com']
    
    def start_requests(self):
        self.header_dict = {
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
        
        yield scrapy.Request(url='http://www.pm25.com/rank.html',
                             callback=self.parse,
                             method='GET',
                             headers=self.header_dict)

    def parse(self, response):
        sub_select = response.xpath('''//ul[contains(@class, "pj_area_data_details") and contains(@class, "rrank_box")]
        /li[contains(@class, "pj_area_data_item")]''')
        for sub in sub_select:
            item = CitiesRankItem()
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
            yield scrapy.Request(url=item['link'],
                                 callback=self.city_detail_parse,
                                 method='GET',
                                 headers=self.header_dict)
            
    def city_detail_parse(self, response):
        '''
        中国标准
        '''
        sub_ul_china = response.xpath('//ul[1][@class="pj_area_data_details"]')
        sub_li_list = sub_ul_china.xpath('./li[contains(@class, "pj_area_data_item")]')
        for sub_li in sub_li_list:
            item = CityItem()
            item['city'] = response.xpath('//span[@class="city_name"]/text()').extract()[0]
            item['standard'] = u'中国标准'.encode('utf-8')
            item['location'] = sub_li.xpath('./a[@class="pjadt_location"]/text()').extract()[0]
            item['aqi'] = sub_li.xpath('./span[@class="pjadt_aqi"]/text()').extract()[0]
            item['quality'] = sub_li.xpath('./span[@class="pjadt_quality"]/em/text()').extract()[0]
            item['pollution'] = sub_li.xpath('./a[@class="pjadt_wuranwu"]/text()').extract()[0]
            item['pm25'] = sub_li.xpath('./span[@class="pjadt_pm25"]/text()').extract()[0]
            item['pm25'] = item['pm25']+sub_li.xpath('./span[@class="pjadt_pm25"]/em/text()').extract()[0]
            item['pm10'] = sub_li.xpath('./span[@class="pjadt_pm10"]/text()').extract()[0]
            item['pm10'] = item['pm25']+sub_li.xpath('./span[@class="pjadt_pm10"]/em/text()').extract()[0]
            item['check_time'] = response.xpath('//div[@class="citydata_updatetime"]/text()').extract()[0]
            yield item
            
        '''
        美国标准
        '''
        sub_ul_usa = response.xpath('//ul[2][@class="pj_area_data_details"]')
        sub_li_list = sub_ul_usa.xpath('./li[contains(@class, "pj_area_data_item")]')
        for sub_li in sub_li_list:
            item = CityItem()
            item['city'] = response.xpath('//span[@class="city_name"]/text()').extract()[0]
            item['standard'] = u'美国标准'.encode('utf-8')
            item['location'] = sub_li.xpath('./a[@class="pjadt_location"]/text()').extract()[0]
            item['aqi'] = sub_li.xpath('./span[@class="pjadt_aqi"]/text()').extract()[0]
            item['quality'] = sub_li.xpath('./span[@class="pjadt_quality"]/em/text()').extract()[0]
            item['pollution'] = sub_li.xpath('./a[@class="pjadt_wuranwu"]/text()').extract()[0]
            item['pm25'] = sub_li.xpath('./span[@class="pjadt_pm25"]/text()').extract()[0]
            item['pm25'] = item['pm25']+sub_li.xpath('./span[@class="pjadt_pm25"]/em/text()').extract()[0]
            item['pm10'] = sub_li.xpath('./span[@class="pjadt_pm10"]/text()').extract()[0]
            item['pm10'] = item['pm25']+sub_li.xpath('./span[@class="pjadt_pm10"]/em/text()').extract()[0]
            item['check_time'] = response.xpath('//div[@class="citydata_updatetime"]/text()').extract()[0]
            yield item
            
        sub_relevant_list = response.xpath('//a[contains(@class, "pr_item") and contains(@class, "pr_item_level")]')
        for sub in sub_relevant_list:
            item = RelevantCityItem()
            item['city'] = response.xpath('//span[@class="city_name"]/text()').extract()[0]
            item['relevant_city'] = sub.xpath('./p[contains(@class, "pri_left")]/text()').extract()[0]
            item['aqi'] = sub.xpath('./p[contains(@class, "pri_right")]/span/text()').extract()[0]
            item['quality'] = sub.xpath('./p[@class="pri_right"]/b/text()').extract()[0]
            item['check_time'] = response.xpath('//div[@class="citydata_updatetime"]/text()').extract()[0]
            yield item
            
        item = CityLinechartItem()
        item['city'] = response.xpath('//span[@class="city_name"]/text()').extract()[0]
        '''
        正则表达式
        '''
        pattern_time = re.compile(r'data\s:\s\[(.*)\]')
        pattern_aqi = re.compile(r'data:\[(.*)\]')
        res_time_24h_30d = re.findall(pattern_time, response.text)
        res_aqi_usa_china = re.findall(pattern_aqi, response.text)
        
        x_time_24h = []
        x_time_30d = []
        y_aqi_china_24h = []
        y_aqi_china_30d = []
        y_aqi_usa_24h = []
        y_aqi_usa_30d = []
        
        x_time_24h = res_time_24h_30d[0].split(',')
        i = 0
        for x in x_time_24h:
            x_time_24h[i] = x.decode('unicode_escape').encode('utf-8')
            i += 1
        x_time_30d = res_time_24h_30d[1].split(',')
        i = 0
        for x in x_time_30d:
            x_time_30d[i] = x.decode('unicode_escape').encode('utf-8')
            i += 1
        
        y_aqi_usa_24h = res_aqi_usa_china[1].split(',')
        y_aqi_china_24h = res_aqi_usa_china[2].split(',')
        y_aqi_usa_30d = res_aqi_usa_china[4].split(',')
        y_aqi_china_30d = res_aqi_usa_china[5].split(',')
        
        item = CityLinechartItem()
        item['city'] = response.xpath('//span[@class="city_name"]/text()').extract()[0]
        item['x_time_24h'] = x_time_24h
        item['x_time_30d'] = x_time_30d
        item['y_aqi_usa_24h'] = y_aqi_usa_24h
        item['y_aqi_china_24h'] = y_aqi_china_24h
        item['y_aqi_usa_30d'] = y_aqi_usa_30d
        item['y_aqi_china_30d'] = y_aqi_china_30d
        item['check_time'] = response.xpath('//div[@class="citydata_updatetime"]/text()').extract()[0]
        yield item
        
        