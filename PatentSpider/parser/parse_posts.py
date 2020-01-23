'''
Task 2: Parsing
'''
from mrq.task import Task
from mrq.job import queue_job
from mrq.context import connections, log

import requests
from lxml import etree
from fake_useragent import UserAgent
import traceback
from datetime import datetime

from _dber.pg_orm import PageSource, Content
from _dber.config import session

import os
import sys

sys.path.insert(0, os.path.abspath(os.getcwd()+'../'))
sys.path.insert(1, os.path.abspath(os.getcwd()+'../../'))
sys.path.insert(2, os.path.abspath(os.getcwd()+'../../../'))
sys.path.insert(3, os.path.abspath(os.getcwd()+'../../../../'))


class __Parser(Task):  # make sure you give it a name :) 記得給parser一個名字呦
    def run(self, params):
        '''
        Run parser
        parser任務主要是負責解析spider爬下來的源碼，並將其存入數據庫
        '''
        url = params['url']
        # 確認內容是否有備存過
        # 這個目的是確定我們沒有重複的數據，如果有存過的話，我們就不要再加新的數據，更新現有的就好
        sess = session()
        added = sess.query(Content).filter_by(url=url).first()
        sess.close()
        if not added:
            # add stuff
            pass

        return True

    def run_wrapped(self, params):
        """ 
        Wrap all calls to tasks in init & safety code. 
        """
        try:
            return self.run(params)
        except Exception as e:
            traceback.print_exc()
            self.requeue_job(
                params, fpath=params['parseTask'], nqueue=params['parsequeue'])
            print(e)

    def retrieve_info(self, url):
        '''
        Parser job based on the source
        Output should be a database object
        在這裡，為了以防再次訪問網站，我們已在spider階段將源碼存入數據庫的pagesource表
        現在，我們只需要將源碼從數據庫中拿出來進行解析就好
        這個函數是parser 的核心，進行主要的解析工作
        '''
        # parsing task given the source, source is retrieved from pagesource
        sess = session()
        ps = sess.query(PageSource).filter_by(url=url).first()
        uid = ps.uid
        source = ps.page_source
        cnt = Content(
            url=url,
            page_source=uid,
            website_name="PUT YOUR WEBSITE HERE",  # <---- put the website name here
            write_date=str(datetime.now())
        )
        sess.commit()
        sess.close()
        # parseing here
        cnt = source
        return cnt

    def insertData(self, cnt):
        '''
        Store result to database
        將解析好的內容存入數據庫
        '''
        try:
            sess = session()
            sess.add(cnt)
            sess.commit()
            return True
        except Exception as e:
            sess.rollback()
            traceback.print_exc()
            print(e)
            return False
        finally:
            sess.close()

    def requeue_job(self, params, fpath=None, nqueue=None):
        '''
        requeue an unfinished job
        '''
        log.warning('Job Failed, re-queue...%s' % params['url'])
        queue_job(fpath, params, queue=nqueue)
