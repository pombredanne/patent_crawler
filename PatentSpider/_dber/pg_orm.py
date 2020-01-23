# table models
# reference samePost.py
from sqlalchemy import Column, Integer, String, Table, Text, Date, Boolean, Time, TIMESTAMP, VARCHAR, func
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
metadata = Base.metadata
'''
two base tables:
PageSource -- store results from spider
Content -- store results from parser
本程式用的表將於此處定義
Base class中每一行是一個Column
根據需求來改變及增加表
'''
# modify tables according to the information needed to be retrieved


class PageSource(Base):
    __tablename__ = "[name]_pagesource" # 這個為表名根據要爬的網站來命名
    uid = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String)
    collection_time = Column(TIMESTAMP, nullable=True,
                             server_default=func.now())
    page_source = Column(VARCHAR)
    flag = Column(String)
    write_date = Column(Date)

    def __repr__(self):
        return f"[Name] Source(Url: '{self.url}', Write Date: '{self.write_date})'"


class Content(Base):
    __tablename__ = "[name]_content"
    __table_args__ = {"useexisting": False}
    uid = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=True)
    author = Column(String)
    #post_date = Column(String)
    public_time = Column(String())  # post_date
    collection_time = Column(TIMESTAMP, nullable=True,
                             server_default=func.now())
    # page_source = Column(VARCHAR)
    update_time = Column(TIMESTAMP)
    page_source = Column(Integer, nullable=True)
    content = Column(String)  # brief
    website_name = Column(String)
    channel_name = Column(String)
    title = Column(String)
    topic = Column(String)
    tag = Column(String)  # category
    meta_keywords = Column(String)
    write_date = Column(String)
    flag = Column(String)
    pic = Column(String)  # image_url

    def __repr__(self):
        return f"[Name] Content(Title: '{self.title}', Post Date: '{self.public_time}')"
