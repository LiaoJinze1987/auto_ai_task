# 处理dispatcher对应的任务
from local_manager import LocalManager

class IntentManager:

    def __init__(self):
        self.local_manager = LocalManager()

    def local_search(self, query: str):
        return self.local_manager.search_files(query)

    def user_task(self, task: str):
        print()

    def scheduled_task(self, task: str, time: str):
        print()