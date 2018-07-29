# -*- coding: utf-8 -*-

# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import os

import pandas as pd
from scrapy import Spider
from scrapy.http import Request

import json
from datetime import datetime



from meituan.models import sdb_connect, mdb_connect

from meituan.items import SubAreaFoodTypeItem, ShopItem, FoodItem, DealListItem, CommentItem, TagItem

from meituan.settings import PERIOD, CITYDBNAME, SAFLOGFILE, DB

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
    saflogfile = SAFLOGFILE

    def parse(self, response):
        SubAreaFoodType = getAllSubAreaFoodType(response, self.city)
        
        
        for i in SubAreaFoodType:
            i.pop('id')
            yield SubAreaFoodTypeItem(**i)
        

        for i in SubAreaFoodType:
            meta = {}
            meta['subAreaFoodType'] = i['city']+'\t' + i['area'] + '\t' + i['subArea'] + '\t' + i['foodType']
            yield Request(i['url'], meta = meta, callback =self.parse_subAreaFoodPage)



    def parse_subAreaFoodPage(self, response):
        data = response.xpath('//script/text()').extract()[-2].replace('window._appState = ', '')[:-1]

        if '"errorMsg":"403"' in data:
            print('Banned by Meituan!!! No Restaurants!')
            print(response.url)
            return None

        try:
            info = json.loads(data)['poiLists']
            log = str(info['totalCounts']) + '\t' + response.meta['subAreaFoodType'] + '\t' + self.period + '\n'
            print(log)
        
            with open(self.saflogfile, 'a') as f:
                f.write(log)

            if info['totalCounts']:

                for shop in info['poiInfos']:
                    shop.pop('dealList')
                    shop['name'] = shop.pop('title')
                    yield ShopItem(timestamp = datetime.now(), status = 0, 
                                   period = self.period,
                                   subAreaFoodTypeUrl = response.url,
                                   url = self.base_url + str(shop['poiId']),
                                   **shop)
        except:
            print(json.loads(data)['poiLists'])



class ShopSpider(Spider):
    period = PERIOD

    def setEngine(self):
        if DB == 'sqlite':
            self.engine = sdb_connect(os.getcwd()+'/db', name = self.citydbname)
        elif DB == 'mysql':
            self.engine = mdb_connect(name = self.citydbname)

    def parse(self, response, inside = True):
        self.setEngine() # then we can get a new self.engine
        df = pd.read_sql('Select url, frontImg, allCommentNum from Shops where status = 0', self.engine)
        print('There are', len(df), 'shops left <----- (0.0)/')
        if inside:
            for ind, row in df.iterrows():
                if not ind%500:
                    print(ind, '\tnew shops have been updated')
                item = row.to_dict()
                url = item.pop('url')

                meta = {'brefRequestshop': item } #TODO
                
                yield Request(url, meta = meta, callback =self.parse_shopPage)
        else:
            for ind, row in df.iterrows():
                if not ind%500:
                    print(ind, '\tnew shops have been updated')
                item = row.to_dict()
                url = item.pop('url')

                meta = {'brefRequestshop': item } #TODO
                
                yield url, meta

        # clear??
        number = pd.read_sql('Select count(*) from Shops where status = 0', self.engine).values[0][0] 
        print('Still left:\t', number)
        #if number.values[0][0] is not 0:
            #self.parse(self, response)
 

    def parse_shopPage(self, response):
        # deal shop information
        # and 
        # food information
        # and
        # dealList information
        # print(response.text)
        data = response.xpath('//script/text()').extract()#
        # print(data)

        if len(data) == 0:
            with open('errors_type1.txt', 'w') as f:
                f.write(response.text)
            print(datetime.now(), ':', response.status, '-----> No output ------------------(#.#).orz!')
            print(datetime.now(), ':', response.url)
            return None
        
        data = data[-2].replace('window._appState = ', '')[:-1]
        # print(data)

        if '"errorMsg":"403"' in data:
            print(datetime.now(), ':','Banned by Meituan!!! No Shop Info!')
            print(datetime.now(), ':', response.url)
            return None

        try:
            data = json.loads(data)
        except:
            with open('errors_type2.txt', 'w') as f:
                f.write(response.text)

            if '验证中心' in response.text:
                print(datetime.now(), ':','This response is a 验证中心 --------------(#.#).orz!')
                # print(datetime.now(), ':', response.url)
            
            return None

        shop = data['detailInfo']
        for i in ['showStatus', 'extraInfos']:
            try:
                shop.pop(i)
            except:
                pass

        
        newshop = {**response.meta['brefRequestshop'], **shop }
        yield ShopItem(timestamp = datetime.now(), 
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





class CommentSpider(Spider):
    
    base_url = "http://www.meituan.com/meishi/"


    def parse_CommentsTags(self, response):
        pass




# SZ

class SZSpider(MeituanSpider):
    name = 'sz'
    city = '深圳'
    start_urls = (
            "http://sz.meituan.com/meishi/",
            )
    base_url = "http://www.meituan.com/meishi/"


class SZShopSpider(ShopSpider):
    name = 'sz_shop'
    city = '深圳'
    citydbname = CITYDBNAME
    start_urls = (
            "http://baidu.com",
            )
    base_url = "http://www.meituan.com/meishi/"



# ZK

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


