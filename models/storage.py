import json
import os
from config import USERS_FILE, CHECKINS_FILE, QUOTES_FILE


class JSONStorage:
    """JSON 数据存储基类"""

    @staticmethod
    def load_data(file_path, default=None):
        """加载 JSON 数据"""
        if default is None:
            default = {}
        try:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return default

    @staticmethod
    def save_data(file_path, data):
        """保存 JSON 数据"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class UserStorage(JSONStorage):
    """用户数据存储"""

    @staticmethod
    def get_all():
        return JSONStorage.load_data(USERS_FILE, {})

    @staticmethod
    def save_all(users):
        JSONStorage.save_data(USERS_FILE, users)

    @staticmethod
    def get_by_id(user_id):
        users = UserStorage.get_all()
        return users.get(str(user_id))

    @staticmethod
    def get_by_username(username):
        users = UserStorage.get_all()
        for user in users.values():
            if user.get('username') == username:
                return user
        return None

    @staticmethod
    def create(user_data):
        users = UserStorage.get_all()
        user_id = max([int(k) for k in users.keys()], default=0) + 1
        user_data['id'] = user_id
        users[str(user_id)] = user_data
        UserStorage.save_all(users)
        return user_data

    @staticmethod
    def update(user_id, user_data):
        users = UserStorage.get_all()
        if str(user_id) in users:
            users[str(user_id)].update(user_data)
            UserStorage.save_all(users)
            return users[str(user_id)]
        return None


class CheckinStorage(JSONStorage):
    """签到数据存储"""

    @staticmethod
    def get_all():
        return JSONStorage.load_data(CHECKINS_FILE, {})

    @staticmethod
    def save_all(checkins):
        JSONStorage.save_data(CHECKINS_FILE, checkins)

    @staticmethod
    def get_by_user(user_id):
        checkins = CheckinStorage.get_all()
        return checkins.get(str(user_id), [])

    @staticmethod
    def add_checkin(user_id, checkin_data):
        checkins = CheckinStorage.get_all()
        user_checkins = checkins.get(str(user_id), [])
        checkin_id = max([c.get('id', 0) for c in user_checkins], default=0) + 1
        checkin_data['id'] = checkin_id
        checkin_data['user_id'] = user_id
        user_checkins.append(checkin_data)
        checkins[str(user_id)] = user_checkins
        CheckinStorage.save_all(checkins)
        return checkin_data


class QuoteStorage(JSONStorage):
    """话语数据存储"""

    @staticmethod
    def get_all():
        return JSONStorage.load_data(QUOTES_FILE, {"built_in": [], "custom": {}})

    @staticmethod
    def save_all(quotes):
        JSONStorage.save_data(QUOTES_FILE, quotes)

    @staticmethod
    def get_built_in():
        data = QuoteStorage.get_all()
        return data.get('built_in', [])

    @staticmethod
    def get_custom(user_id):
        data = QuoteStorage.get_all()
        custom = data.get('custom', {})
        return custom.get(str(user_id), [])

    @staticmethod
    def get_all_quotes(user_id):
        """获取所有可用话语（内置 + 用户自定义）"""
        built_in = QuoteStorage.get_built_in()
        custom = QuoteStorage.get_custom(user_id)
        return built_in + custom

    @staticmethod
    def add_custom(user_id, content, category="个人"):
        data = QuoteStorage.get_all()
        if 'custom' not in data:
            data['custom'] = {}
        if str(user_id) not in data['custom']:
            data['custom'][str(user_id)] = []

        quote_id = max([q.get('id', 0) for q in data['custom'].get(str(user_id), [])], default=0) + 1000
        quote = {
            'id': quote_id,
            'content': content,
            'category': category
        }
        data['custom'][str(user_id)].append(quote)
        QuoteStorage.save_all(data)
        return quote
