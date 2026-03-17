import pytest
import os
from models.ai_quote import AIQuoteStorage


class TestAIQuoteStorage:

    def setup_method(self):
        if os.path.exists(AIQuoteStorage.QUOTES_FILE):
            os.remove(AIQuoteStorage.QUOTES_FILE)

    def teardown_method(self):
        if os.path.exists(AIQuoteStorage.QUOTES_FILE):
            os.remove(AIQuoteStorage.QUOTES_FILE)

    def test_get_by_user_empty(self):
        quotes = AIQuoteStorage.get_by_user(1)
        assert quotes == []

    def test_add_quote(self):
        result = AIQuoteStorage.add_quote(1, "娃啊，记得吃饭", "妈妈", "四川话")
        assert result['id'] == 1
        assert result['content'] == "娃啊，记得吃饭"

    def test_get_by_user_order(self):
        AIQuoteStorage.add_quote(1, "第一条", "妈妈", "四川话")
        import time
        time.sleep(0.01)
        AIQuoteStorage.add_quote(1, "第二条", "妈妈", "四川话")

        quotes = AIQuoteStorage.get_by_user(1)
        assert quotes[0]['content'] == "第二条"  # 最新在前
        assert quotes[1]['content'] == "第一条"
