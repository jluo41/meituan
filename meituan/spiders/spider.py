# -*- coding: utf-8 -*-

# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Spider
from scrapy.http import Request

import json
from datetime import datetime



from meituan.items import SubAreaFoodTypeItem, ShopItem, FoodItem, DealListItem, CommentItem, TagItem

from meituan.settings import PERIOD




## some util functions



def getAllSubAreaFoodType(response, city):
    foodcl = [i for i in response.xpath('//ul[@class="more clear"]/li/a/text()').extract()]
    foodli = [i[:-1] for i in response.xpath('//ul[@class="more clear"]/li/a/@href').extract() if '/c' in i]


    foodClass = dict(zip(foodcl, foodli))

    # pprint(foodClass)

    data = response.xpath('//script/text()').extract()[-2].replace('window._appState = ', '')[:-1]
    try:
    	data = json.loads(data)
    except:
    	print(data)
    	return 
    #data.pop('comFooter')
    #data.pop('comHeader')
    #data.pop('$meta')
    areas = data['filters']['areas']
    #pprint()#['poiLists'])
    
    CitySubAreaFoodTypeData = []
    # city = '深圳'
    for a in areas:
        # a: area, can be 福田
        subAreas = a['subAreas']
        subAreaList = [ {'city': city, 'area': a['name'], 'subArea': i['name'], 'id': i['id']} for i in a['subAreas'] if i['name'] != '全部']

        for subArea in subAreaList:
            CitySubAreaFoodTypeData.extend([ {'foodType': food, 'url': foodClass[food]+ 'b' + str(subArea['id']) + '/', **subArea } for food in foodClass])

    return CitySubAreaFoodTypeData



class MeituanSpider(Spider):

    period = PERIOD

    def parse(self, response):
        SubAreaFoodType = getAllSubAreaFoodType(response, self.city)
        
        
        for i in SubAreaFoodType:
            i.pop('id')
            yield SubAreaFoodTypeItem(**i)
        

        for i in SubAreaFoodType:
            meta = {}
            meta['subAreaFoodType'] = i['subArea'] + '-' + i['foodType']
            yield Request(i['url'], meta = meta, callback =self.parse_subAreaFoodPage)



    def parse_subAreaFoodPage(self, response):
        data = response.xpath('//script/text()').extract()[-2].replace('window._appState = ', '')[:-1]

        if '"errorMsg":"403"' in data:
            print('Banned by Meituan!!! No Restaurants!')
            print(response.url)
            return None

        info = json.loads(data)['poiLists']
        if info['totalCounts']:
            for shop in info['poiInfos']:
                shop.pop('dealList')
                shop['name'] = shop.pop('title')
                yield ShopItem(timestamp = datetime.now(), status = 0, 
                               period = self.period,
                               subAreaFoodTypeUrl = response.url,
                               url = self.base_url + str(shop['poiId']),
                               **shop)

            for shop in info['poiInfos']:
                response.meta['brefRequestshop'] = {i: shop[i] for i in ['frontImg', 'allCommentNum']}
                response.meta['subAreaFoodTypeUrl'] = response.url
                yield Request(self.base_url + str(shop['poiId']), meta = response.meta, callback =self.parse_shopPage)
        
        else:
            print('No shops in', response.meta['subAreaFoodType'])

        

    def parse_shopPage(self, response):
        # deal shop information
        # and 
        # food information
        # and
        # dealList information
        data = response.xpath('//script/text()').extract()[-2].replace('window._appState = ', '')[:-1]

        if '"errorMsg":"403"' in data:
            print('Banned by Meituan!!! No Shop Info!')
            print(response.url)
            return None

        data = json.loads(data)

        shop = data['detailInfo']
        for i in ['showStatus', 'extraInfos']:
            try:
                shop.pop(i)
            except:
                pass

        newshop = {**response.meta['brefRequestshop'], **shop }
        yield ShopItem(timestamp = datetime.now(), 
                       subAreaFoodTypeUrl = response.meta['subAreaFoodTypeUrl'],
                       status = 1, 
                       period = self.period,
                       url = response.url,
                       **newshop)

        
        for food in data['recommended']:
            food.pop('frontImgUrl')
            food['food_id'] = food.pop('id')
            yield FoodItem(timestamp = datetime.now(), 
                           period = self.period,
                           poiId = shop['poiId'],
                           **food)

        

        for dealList in data['dealList']['deals']:
            dealList['dealList_id'] = dealList.pop('id')
            dealList['name'] = dealList.pop('title')
            
            yield DealListItem(timestamp = datetime.now(), 
                               period = self.period,
                               poiId = shop['poiId'],
                               **dealList)


    def parse_CommentsTags(self, response):
        pass



class SZSpider(MeituanSpider):
    name = 'sz'
    city = '深圳'
    start_urls = (
            "http://sz.meituan.com/meishi",
            )
    base_url = "http://www.meituan.com/meishi/"



