# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item, Field


class SubAreaFoodTypeItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = Field()

    area = Field()
    subArea = Field()
    foodType = Field()
    
    url = Field()


class ShopItem(Item):
    subAreaFoodTypeUrl = Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    poiId = Field()    # shop's meituan shop id
    name  = Field()     # shop's name, also, it is title
    
    avgScore = Field() # avgScore
    avgPrice = Field() 
    allCommentNum = Field()
    
    frontImg = Field() # shop's image
    address = Field()
    
    # after requesting shop's URL
    brandId  = Field()
    brandName= Field()
    
    openTime = Field()
    phone    = Field()
    
    latitude = Field()
    longitude= Field()
    
    hasFoodSafeInfo = Field()
    isMeishi = Field()
    
    
    url = Field()
    
    # Time Index
    timestamp = Field() # will be update after requesting
    period    = Field()     # set as constant
    
    status = Field() # default is 0, 



class FoodItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    poiId     = Field()
    food_id = Field()    # shop's meituan shop id
    name  = Field()     # shop's name, also, it is title
    
    price = Field() # avgScore
    
    timestamp = Field() # will be update after requesting
    period    = Field()     # set as constant


class DealListItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    poiId     = Field()
    
    dealList_id = Field()    # shop's meituan shop id
    name    = Field()     # shop's name, also, it is title
    soldNum = Field()  
    value   = Field()  
    price   = Field() # avgScore
    frontImgUrl = Field()
    
    timestamp = Field() # will be update after requesting
    period    = Field()     # set as constant


# TODO in the future
class CommentItem(Item):
    poiId     = Field()

    alreadyZzz = Field()
    
    anonymous = Field()
    
    avgPrice  = Field()
    
    comment   = Field()
    
    commentTime = Field()
    
    dealEndtime = Field()

    hilignt = Field()

    menu    = Field()

    merchantComment = Field()
    
    picUrls = Field()

    quality = Field()

    readCnt = Field()

    replyCnt= Field()

    reviewId= Field()

    star    = Field()

    uType   = Field()

    userId  = Field()

    userLevel= Field()

    userName = Field()

    userUrl  = Field()

    zanCnt   = Field()

    
class TagItem(Item):

    tag   = Field()
    count = Field()
    
    # ItemName = Field()

    timestamp = Field()
    period    = Field()

    poiId     = Field()
    


