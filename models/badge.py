import json
import os
from datetime import datetime
from config import DATA_DIR


class BadgeStorage:
    """勋章数据存储"""

    BADGES_FILE = os.path.join(DATA_DIR, 'badges.json')

    # 勋章定义
    BADGE_DEFINITIONS = {
        # 时间里程碑系列
        'day_1': {'name': '🌱 初来乍到', 'description': '离开家乡的第一天', 'category': 'time'},
        'day_7': {'name': '📅 七日维新', 'description': '坚持了一周', 'category': 'time'},
        'day_30': {'name': '🌙 满月之约', 'description': '离家一个月了', 'category': 'time'},
        'day_100': {'name': '🔄 百日征程', 'description': '百日纪念', 'category': 'time'},
        'day_180': {'name': '💫 半年光阴', 'description': '半年过去了', 'category': 'time'},
        'day_365': {'name': '🏆 一年归期', 'description': '离家一整年', 'category': 'time'},

        # 签到连续系列
        'streak_3': {'name': '🔥 三日热', 'description': '开始上瘾了', 'category': 'streak'},
        'streak_7': {'name': '⚡ 周冠军', 'description': '坚持一周！', 'category': 'streak'},
        'streak_15': {'name': '🌟 半月谈', 'description': '半个月不间断', 'category': 'streak'},
        'streak_30': {'name': '💪 月全勤', 'description': '整月打卡', 'category': 'streak'},
        'streak_100': {'name': '👑 签到之王', 'description': '传奇！', 'category': 'streak'},

        # 特殊成就系列
        'late_night': {'name': '🌙 深夜未眠', 'description': '这么晚还没睡', 'category': 'special'},
        'early_bird': {'name': '🌅 早起鸟儿', 'description': '起得真早', 'category': 'special'},
        'quote_master': {'name': '📝 思乡达人', 'description': '文采斐然', 'category': 'special'},
    }

    @staticmethod
    def get_all():
        """获取所有用户的勋章数据"""
        try:
            if os.path.exists(BadgeStorage.BADGES_FILE):
                with open(BadgeStorage.BADGES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
        return {}

    @staticmethod
    def save_all(badges):
        """保存勋章数据"""
        with open(BadgeStorage.BADGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(badges, f, ensure_ascii=False, indent=2)

    @staticmethod
    def get_by_user(user_id):
        """获取用户的勋章列表"""
        badges = BadgeStorage.get_all()
        return badges.get(str(user_id), [])

    @staticmethod
    def add_badge(user_id, badge_id):
        """给用户添加勋章"""
        badges = BadgeStorage.get_all()
        user_badges = badges.get(str(user_id), [])

        # 检查是否已获得
        for badge in user_badges:
            if badge.get('badge_id') == badge_id:
                return None  # 已存在，不重复添加

        new_badge = {
            'badge_id': badge_id,
            'earned_at': datetime.now().isoformat()
        }
        user_badges.append(new_badge)
        badges[str(user_id)] = user_badges
        BadgeStorage.save_all(badges)
        return new_badge

    @staticmethod
    def get_definition(badge_id):
        """获取勋章定义"""
        return BadgeStorage.BADGE_DEFINITIONS.get(badge_id)

    @staticmethod
    def get_all_definitions():
        """获取所有勋章定义"""
        return BadgeStorage.BADGE_DEFINITIONS
