# 意图分析器
from intent_manager import IntentManager

class IntentDispatcher:

    def __init__(self):
        self.manager = IntentManager()

    def dispatch(self, intent: dict):
        _type = intent["type"]
        if _type == "chat":
            return intent["reply"]
        if _type == "local_search":
            return self.handle_local_search(intent)
        if _type == "task":
            return self.handle_task(intent)
        if _type == "scheduled_task":
            return self.handle_scheduled_task(intent)
        if _type == "compound_task":
            return self.handle_compound_task(intent)
        raise ValueError(
            f"未知的 intent type: {_type}"
        )

    def handle_local_search(self, intent: dict):
        query = intent["query"]
        return self.manager.local_search(query)

    def handle_task(self, intent: dict):
        task = intent["task"]
        self.manager.user_task(task)

    def handle_scheduled_task(self, intent: dict):
        task = intent["task"]
        time = intent["time"]
        self.manager.scheduled_task(task, time)

    def handle_compound_task(self, intent: dict):
        steps = intent["steps"]
