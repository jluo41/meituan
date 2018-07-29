# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from sqlalchemy.orm import sessionmaker

from datetime import datetime

from meituan.items import SubAreaFoodTypeItem, ShopItem, FoodItem, DealListItem, CommentItem, TagItem
from meituan.models import sdb_connect, mdb_connect, create_table
from meituan.models import SubAreaFoodType, Shop, Food, DealList, Comment, Tag
from meituan.settings import DB
from meituan.settings import CITYDBNAME

class MeituanPipeline(object):

    def __init__(self):
        if DB == 'sqlite':
            engine = sdb_connect(os.getcwd()+'/db', name = CITYDBNAME)
        elif DB == 'mysql':
            engine = mdb_connect(name = CITYDBNAME)
        create_table(engine)
        Session = sessionmaker(bind = engine)
        self.session = Session()

    def process_item(self, item, spider):


        # SubAreaFoodType
        if isinstance(item, SubAreaFoodTypeItem):
            
            subAreaFoodType = self.session.query(SubAreaFoodType).filter_by(url = item['url']).first()
            

            if subAreaFoodType is not None:
                # if there is a same item
                print(datetime.now(), ': exits already! <---o---------(-.-) : subAreaFoodType ')
                return item
                # end here


            else:
                subAreaFoodType = SubAreaFoodType(**item)

                try:
                    self.session.add(subAreaFoodType)
                except:
                    self.session.rollback()
                    raise
                
                self.session.commit()

                return item


        # Shop
        elif isinstance(item, ShopItem):
            # to avoid the duplicates

            if item['status'] == 0:

                sameshop = self.session.query(Shop).filter_by(period= item['period'], 
                                                              poiId = item['poiId'],
                                                              ).first() # same period, same shop, 
                                                                        # same status 1, 
                                                                        # don't need to modify anymore
                                                                        # then pass


                if sameshop:
                    print(datetime.now(), ': exits already! <---o---------(-.-) : ShopItem')
                    return item 
                    # end here
                else:

                    subAreaFoodType = self.session.query(SubAreaFoodType).filter_by(url = item['subAreaFoodTypeUrl']).first()
                
                    del item['subAreaFoodTypeUrl']

                    shop = Shop(**item)

                    try:
                        self.session.add(shop)
                    except:
                        self.session.rollback()
                        raise

                    if subAreaFoodType is not None:
                        subAreaFoodType.shops.append(shop)

                    self.session.commit()
                    return item


            elif item['status'] == 1:

                shop = self.session.query(Shop).filter_by(period = item['period'],
                                                          poiId  = item['poiId'],
                                                          status = 0).first()

                if shop is not None:
                    for i in item:
                        setattr(shop, i, item[i])
                    self.session.commit()
                    print(datetime.now(), ': Update shop! <------======------ ~(0.0)//~~!')
                    return item

                else:
                    print(datetime.now(), ': Update shop? not. Useless Full ShopItem!!!')



        # Food
        elif isinstance(item, FoodItem):
            samefood = self.session.query(Food).filter_by(period  = item['period'], 
                                                          food_id = item['food_id'] ,
                                                          poiId   = item['poiId']                                                         
                                                          ).first() # same period, same shop, 
                                                                    
                             
            if samefood is not None:
                print(datetime.now(), ': exits already! <---o---------(-.-) : FoodItem ')
                return item 

            else:
                # first get its parents
                shop = self.session.query(Shop).filter_by(poiId = item['poiId']).first()
                
                food = Food(**item)

                try:
                    self.session.add(food)
                except:
                    self.session.rollback()
                    raise

                if shop is not None:
                    shop.foods.append(food)

                self.session.commit()
                return item

        # DealList
        elif isinstance(item, DealListItem):
            samedealList = self.session.query(DealList).filter_by(period= item['period'], 
                                                                  dealList_id = item['dealList_id'] ,
                                                                  poiId = item['poiId']                                                         
                                                                  ).first() # same period, same shop, 
                                                                    # same status 1, 
                             
            if samedealList is not None:
                print(datetime.now(), ': exits already! <---o---------(-.-) : DealListItem')
                return item 

            else:
                # first get its parents
                shop = self.session.query(Shop).filter_by(poiId = item['poiId'], period = item['period']).first()
                
                dealList = DealList(**item)

                try:
                    self.session.add(dealList)
                except:
                    self.session.rollback()
                    raise

                if shop is not None:
                    shop.dealLists.append(dealList)

                self.session.commit()
                return item

        # other condition
        else:
            return item
            #pass



