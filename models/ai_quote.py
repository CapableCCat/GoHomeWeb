import json
import os
from datetime import datetime
from config import DATA_DIR


class AIQuoteStorage:
    """AI 问候数据存储"""

    QUOTES_FILE = os.path.join(DATA_DIR, 'ai_quotes.json')

    @staticmethod
    def get_all():
        """获取所有用户的 AI 问候数据"""
        try:
            if os.path.exists(AIQuoteStorage.QUOTES_FILE):
                with open(AIQuoteStorage.QUOTES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return {}

    @staticmethod
    def save_all(quotes):
        """保存 AI 问候数据"""
        with open(AIQuoteStorage.QUOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump(quotes, f, ensure_ascii=False, indent=2)

    @staticmethod
    def get_by_user(user_id, limit=None):
        """获取用户的 AI 问候列表"""
        quotes = AIQuoteStorage.get_all()
        user_quotes = quotes.get(str(user_id), [])

        # 按时间倒序排列
        user_quotes = sorted(
            user_quotes,
            key=lambda x: x.get('created_at', ''),
            reverse=True
        )

        if limit:
            user_quotes = user_quotes[:limit]

        return user_quotes

    @staticmethod
    def add_quote(user_id, content, family_role, dialect):
        """添加 AI 问候记录"""
        quotes = AIQuoteStorage.get_all()
        user_quotes = quotes.get(str(user_id), [])

        quote_id = max([q.get('id', 0) for q in user_quotes], default=0) + 1

        new_quote = {
            'id': quote_id,
            'user_id': user_id,
            'content': content,
            'family_role': family_role,
            'dialect': dialect,
            'created_at': datetime.now().isoformat()
        }
        user_quotes.append(new_quote)
        quotes[str(user_id)] = user_quotes
        AIQuoteStorage.save_all(quotes)
        return new_quote
