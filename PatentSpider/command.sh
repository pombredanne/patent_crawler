#!/bin/bash
# 使用前：啟動虛擬環境
# 如果沒有虛擬環境：
python3 -m virtualenv venv
# 安裝成功之後 在主目錄之下啟動
source venv/bin/activate

# 第一個函數為 栈 的名稱 要與task_executor 中命名的栈名一致才能順利啟動任務喔
# 第一步：排任務
mrq-run --queue taskexecutor task_executor.Execute_Crawl

# 第二步：啟動mrq worker
# mrq-worker 第一個函數也為 栈 的名稱， --greenlet 是worker 數 這裡都先定義為一個，可是可以根據需求更改增加
# 每個任務種類都會有一個要定義的栈，同樣的也需要一個mrq-worker
# 在這個步驟要講所有的mrq-worker啟動所有種類的任務才能被完成
mrq-worker taskexecutor --greenlet 1 & mrq-worker crawl_posts --greenlet 1 & mrq-worker parse_posts --greenlet 1 &
# last worker works on the default queue, in charge of taking care of extraneous tasks on the dashboard