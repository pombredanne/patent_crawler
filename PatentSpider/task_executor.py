'''
Meta-Task:
Execute and coordinate Spider and Parser

這是啟動任務的關鍵中介，程式啟動時會從這裡開始
task_executor的主要功能是將任務及任務所需的資料(如url)交給spider去執行
spider 完成後自己會交棒給parser,這一部分就不需要task_executor 來了
'''
import time
import subprocess
import traceback

from mrq.task import Task
from mrq.job import queue_job
from mrq.context import connections, log

import sys
import os
sys.path.insert(0, os.path.abspath(os.getcwd()+'../../../'))
sys.path.insert(1, os.path.abspath(os.getcwd()+'../../../../'))


class Execute_Crawl(Task):
    '''
    Execution of two tasks: crawl and parse
    '''

    def __init__(self):
        super(Execute_Crawl, self).__init__()

    def exec_push_work(self, url):
        # import subprocess
        # modify arguments
        # 這些是會傳下去給spider的函數 除了spider需要用的之外，還包括所有栈名以及其任務的路徑
        # 如果有更改栈名請於此更改
        args = {
            'url': url,
            'spiderTask': 'spider.spider.__Spider',
            'spiderqueue': 'crawl_posts',
            'parseTask': 'parser.parse_posts.__Parser',
            'parsequeue': 'parse_posts'
        }
        # task = ['spider.spider_crawl.LcSpider']
        # command = ['mrq-run'] + task + args
        # '--queue', 'crawl_posts'
        # subprocess.Popen(command)
        queue_job(args['spiderTask'], args, queue=args['spiderqueue'])

    def run(self, params):
        '''
        Enqueue spider jobs
        '''
        # 我們在這裡開始分發任務
        url = None
        self.exec_push_work(url)

    def run_wrapped(self, params):
        """
        Wrap all calls to tasks in init & safety code.
        這是保險，如果執行task_executor有意外這裡會重新啟動
        """
        try:
            return self.run(params)
        except Exception as e:
            traceback.print_exc()
            self.requeue_job(
                params, fpath='task_executor.Execute_Crawl', nqueue='taskexecutor')
            print(e)

    def requeue_job(self, params, fpath=None, nqueue=None):
        '''
        requeue an unfinished job
        run_wrapped的helper function
        '''
        log.warning('Job Failed, re-queue...%s' % params['url'])
        queue_job(fpath, params, queue=nqueue)
