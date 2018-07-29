import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Table, Text, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


def sdb_connect(basedir, name = 'data'):
    return create_engine('sqlite:///'+os.path.join(basedir, name + '.sqlite'))

def mdb_connect(name):
    MySQL_DB = 'mysql+pymysql://root:@localhost:3306/name?charset=utf8'
    return create_engine(MySQL_DB)


Base = declarative_base()

def create_table(engine):
    Base.metadata.create_all(engine)

## Schema

class SubAreaFoodType(Base):
    # all the values in this table are constant
    # not time-varying
    __tablename__ = 'SubAreaFoodTypes'
    id = Column(Integer, primary_key=True)
    
    city = Column(Text)    
    area = Column(Text)
    subArea = Column(Text)
    foodType = Column(Text)
    
    url = Column(Text)
    
    # 1-->N, here is 1
    shops = relationship("Shop", back_populates = 'subAreaFoodType')


class Shop(Base):
    __tablename__ = 'Shops'
    id = Column(Integer, primary_key=True)
    
    # before requesting shop's URL
    
    poiId = Column(Integer)    # shop's meituan shop id
    name  = Column(Text)     # shop's name, also, it is title
    
    avgScore = Column(Text) # avgScore
    avgPrice = Column(Text) 
    allCommentNum = Column(Integer)
    
    frontImg = Column(Text) # shop's image
    address = Column(Text)
    
    # after requesting shop's URL
    brandId  = Column(Text)
    brandName= Column(Text)
    
    openTime = Column(Text)
    phone    = Column(Text)
    
    latitude = Column(Text)
    longitude= Column(Text)
    
    hasFoodSafeInfo = Column(Text)
    isMeishi = Column(Text)
    
    
    url = Column(Text)
    
    # Time Index
    timestamp = Column(DateTime) # will be update after requesting
    period    = Column(Text)     # set as constant
    
    status = Column(Integer) # default is 0, 
                             # meaning not yet requesting
                             # will be updated after requesting,
                             # and be set as 1.
    
    
    # 1-->N, here is 1
    foods    = relationship("Food", back_populates = 'shop')
    
    # 1-->N, here is 1
    comments = relationship("Comment", back_populates = 'shop')
    
    # 1-->N, here is 1
    tags = relationship("Tag", back_populates = 'shop')
    
    # 1-->N, here is 1
    dealLists = relationship("DealList", back_populates = 'shop')

    # 1-->N SubAreaFoodType --> Shops, here is n
    subAreaFoodType_id = Column(Integer, ForeignKey("SubAreaFoodTypes.id"))
    subAreaFoodType    = relationship("SubAreaFoodType", back_populates="shops")



class Food(Base):
    __tablename__ = 'Foods'
    id = Column(Integer, primary_key=True)
    food_id = Column(Integer)
    poiId = Column(Integer)    # shop's meituan shop id
    

    name  = Column(Text)
    price = Column(Text)
    
    timestamp = Column(DateTime)
    period    = Column(Text)
    
    # 1-->N SubAreaFoodType --> Shops, here is n
    shop_id = Column(Integer, ForeignKey("Shops.id"))
    shop    = relationship("Shop", back_populates="foods")

    
class DealList(Base):
    __tablename__ = 'DealLists'
    id = Column(Integer, primary_key=True)
    
    dealList_id = Column(Integer)
    poiId = Column(Integer)    # shop's meituan shop id


    name    = Column(Text) # change the title to name
    soldNum = Column(Integer)
    value   = Column(Integer)
    price   = Column(Integer)
    
    frontImgUrl = Column(Text)
    
    timestamp = Column(DateTime)
    period    = Column(Text)
    
    # 1-->N SubAreaFoodType --> Shops, here is n
    shop_id = Column(Integer, ForeignKey("Shops.id"))
    shop    = relationship("Shop", back_populates="dealLists")


# TODO in the future
class Comment(Base):
    __tablename__ = 'Comments'
    id = Column(Integer, primary_key=True)
    userId  = Column(Integer)
    poiId = Column(Integer)


    alreadyZzz = Column(Text)
    
    anonymous = Column(Text)
    
    avgPrice  = Column(Text)
    
    comment   = Column(Text)
    
    commentTime = Column(Text)
    
    dealEndtime = Column(Text)

    hilignt = Column(Text)

    menu    = Column(Text)

    merchantComment = Column(Text)
    
    picUrls = Column(Text)

    quality = Column(Text)

    readCnt = Column(Text)

    replyCnt= Column(Text)

    reviewId= Column(Text)

    star    = Column(Text)

    uType   = Column(Text)

    

    userLevel= Column(Text)

    userName = Column(Text)

    userUrl  = Column(Text)

    zanCnt   = Column(Text)

    # ItemName = Column(Text)

    # 1-->N SubAreaFoodType --> Shops, here is n
    shop_id = Column(Integer, ForeignKey("Shops.id"))
    shop    = relationship("Shop", back_populates="comments")

    
class Tag(Base):
    __tablename__ = 'Tags'
    id = Column(Integer, primary_key=True)
    poiId = Column(Integer)

    
    tag   = Column(Text)
    count = Column(Integer)
    
    # ItemName = Column(Text)

    timestamp = Column(DateTime)
    period    = Column(Text)
    
    # 1-->N SubAreaFoodType --> Shops, here is n
    shop_id = Column(Integer, ForeignKey("Shops.id"))
    shop    = relationship("Shop", back_populates="tags")



