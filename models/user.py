from datetime import datetime, timedelta
from models.storage import UserStorage, CheckinStorage


class User:
    """用户模型"""

    def __init__(self, user_data):
        self.id = user_data.get('id')
        self.username = user_data.get('username')
        self.password_hash = user_data.get('password_hash')
        self.hometown = user_data.get('hometown', '')
        self.current_city = user_data.get('current_city', '')
        self.leave_home_date = user_data.get('leave_home_date')
        self.created_at = user_data.get('created_at')
        # 家人配置字段
        self.family_role = user_data.get('family_role', '妈妈')
        self.nickname = user_data.get('nickname', '')
        self.tone_style = user_data.get('tone_style', '唠叨型')

    def get_days_away_from_home(self):
        """计算离家天数"""
        if not self.leave_home_date:
            return 0
        try:
            leave_date = datetime.strptime(self.leave_home_date, '%Y-%m-%d')
            return (datetime.now() - leave_date).days
        except ValueError:
            return 0

    def get_checkin_stats(self):
        """获取签到统计信息"""
        checkins = CheckinStorage.get_by_user(self.id)
        total_days = len(checkins)

        if total_days == 0:
            return {
                'total_days': 0,
                'current_streak': 0,
                'longest_streak': 0
            }

        # 计算连续签到
        dates = sorted([c['checkin_date'] for c in checkins], reverse=True)
        current_streak = 1
        longest_streak = 1
        temp_streak = 1

        for i in range(1, len(dates)):
            prev_date = datetime.strptime(dates[i-1], '%Y-%m-%d')
            curr_date = datetime.strptime(dates[i], '%Y-%m-%d')
            diff = (prev_date - curr_date).days

            if diff == 1:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            elif diff == 0:
                continue
            else:
                # 检查是否今天签到
                today = datetime.now().strftime('%Y-%m-%d')
                if dates[0] == today:
                    current_streak = temp_streak
                temp_streak = 1

        # 检查今天是否签到
        today = datetime.now().strftime('%Y-%m-%d')
        if dates[0] == today:
            current_streak = longest_streak if longest_streak == temp_streak else temp_streak
        else:
            current_streak = 0

        # 重新计算当前连续签到
        current_streak = self._calculate_current_streak(dates)

        return {
            'total_days': total_days,
            'current_streak': current_streak,
            'longest_streak': longest_streak
        }

    def _calculate_current_streak(self, dates):
        """计算当前连续签到天数"""
        if not dates:
            return 0

        today = datetime.now().date()
        yesterday = today

        streak = 0
        for date_str in dates:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                if date == yesterday or date == today:
                    streak += 1
                    yesterday = date - timedelta(days=1)
                else:
                    break
            except:
                continue
        return streak

    def has_checked_in_today(self):
        """检查今天是否已签到"""
        checkins = CheckinStorage.get_by_user(self.id)
        today = datetime.now().strftime('%Y-%m-%d')
        return any(c['checkin_date'] == today for c in checkins)

    def get_last_checkin(self):
        """获取最后一次签到记录"""
        checkins = CheckinStorage.get_by_user(self.id)
        if not checkins:
            return None
        return max(checkins, key=lambda x: x.get('checkin_time', ''))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'hometown': self.hometown,
            'current_city': self.current_city,
            'leave_home_date': self.leave_home_date,
            'created_at': self.created_at,
            'family_role': self.family_role,
            'nickname': self.nickname,
            'tone_style': self.tone_style
        }
