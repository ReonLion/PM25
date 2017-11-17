# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Pm25Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CitiesRankItem(scrapy.Item):
    ranknum = scrapy.Field()
    quality = scrapy.Field()
    city = scrapy.Field()
    province = scrapy.Field()
    aqi = scrapy.Field()
    pm25 = scrapy.Field()
    link = scrapy.Field()
    check_time = scrapy.Field()
    
class CitiesRank1dayItem(scrapy.Item):
    ranknum = scrapy.Field()
    quality = scrapy.Field()
    city = scrapy.Field()
    province = scrapy.Field()
    aqi = scrapy.Field()
    pm25 = scrapy.Field()
    link = scrapy.Field()
    check_time = scrapy.Field()

class CitiesRank7dayItem(scrapy.Item):
    ranknum = scrapy.Field()
    quality = scrapy.Field()
    city = scrapy.Field()
    province = scrapy.Field()
    aqi = scrapy.Field()
    pm25 = scrapy.Field()
    link = scrapy.Field()
    check_time = scrapy.Field()
    
class CitiesRank30dayItem(scrapy.Item):
    ranknum = scrapy.Field()
    quality = scrapy.Field()
    city = scrapy.Field()
    province = scrapy.Field()
    aqi = scrapy.Field()
    pm25 = scrapy.Field()
    link = scrapy.Field()
    check_time = scrapy.Field()
    
class CityItem(scrapy.Item):
    city = scrapy.Field()
    standard = scrapy.Field()
    location = scrapy.Field()
    aqi = scrapy.Field()
    quality = scrapy.Field()
    pollution = scrapy.Field()
    pm25 = scrapy.Field()
    pm10 = scrapy.Field()
    check_time = scrapy.Field()
    
class CityLinechartItem(scrapy.Item):
    city = scrapy.Field()
    x_time_24h = scrapy.Field()
    x_time_30d = scrapy.Field()
    y_aqi_china_24h =scrapy.Field()
    y_aqi_china_30d = scrapy.Field()
    y_aqi_usa_24h =scrapy.Field()
    y_aqi_usa_30d = scrapy.Field()
    check_time = scrapy.Field()
    
class RelevantCityItem(scrapy.Item):
    city = scrapy.Field()
    relevant_city = scrapy.Field()
    aqi = scrapy.Field()
    quality = scrapy.Field()
    check_time = scrapy.Field()