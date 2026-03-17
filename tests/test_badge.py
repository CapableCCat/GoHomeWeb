import pytest
import os
import json
from models.badge import BadgeStorage


class TestBadgeStorage:

    def setup_method(self):
        """测试前清理"""
        if os.path.exists(BadgeStorage.BADGES_FILE):
            os.remove(BadgeStorage.BADGES_FILE)

    def teardown_method(self):
        """测试后清理"""
        if os.path.exists(BadgeStorage.BADGES_FILE):
            os.remove(BadgeStorage.BADGES_FILE)

    def test_get_by_user_empty(self):
        """测试获取空用户勋章"""
        badges = BadgeStorage.get_by_user(1)
        assert badges == []

    def test_add_badge(self):
        """测试添加勋章"""
        result = BadgeStorage.add_badge(1, 'streak_3')
        assert result is not None
        assert result['badge_id'] == 'streak_3'

    def test_add_duplicate_badge(self):
        """测试重复添加勋章"""
        BadgeStorage.add_badge(1, 'streak_3')
        result = BadgeStorage.add_badge(1, 'streak_3')
        assert result is None  # 返回 None 表示已存在

    def test_get_definition(self):
        """测试获取勋章定义"""
        definition = BadgeStorage.get_definition('streak_3')
        assert definition['name'] == '🔥 三日热'
