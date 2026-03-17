from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from datetime import datetime
from models.user import User
from models.storage import CheckinStorage, QuoteStorage, UserStorage
from models.badge import BadgeStorage
from models.ai_quote import AIQuoteStorage
from utils.quote_generator import QuoteGenerator
from utils.ai_hometown_generator import AIHometownGenerator
from routes.auth import login_required
from config import AI_API_KEY, AI_API_BASE_URL, AI_MODEL

checkin_bp = Blueprint('checkin', __name__)


@checkin_bp.route('/checkin', methods=['GET', 'POST'])
@login_required
def do_checkin():
    """签到打卡"""
    user = User(UserStorage.get_by_id(session['user_id']))

    if request.method == 'POST':
        new_badges = []  # 记录新解锁的勋章

        # 检查今天是否已签到
        if user.has_checked_in_today():
            flash('今天已经签到过了', 'info')
            return redirect(url_for('dashboard.index'))

        # 检查特殊成就勋章
        checkin_time = datetime.now()

        # 深夜未眠勋章 (凌晨 2 点后)
        if checkin_time.hour >= 2:
            badge = BadgeStorage.add_badge(user.id, 'late_night')
            if badge:
                new_badges.append(BadgeStorage.get_definition('late_night'))

        # 早起鸟儿勋章 (早上 6 点前)
        elif checkin_time.hour < 6:
            badge = BadgeStorage.add_badge(user.id, 'early_bird')
            if badge:
                new_badges.append(BadgeStorage.get_definition('early_bird'))

        # 优先尝试 AI 生成家人问候
        quote_content = None
        quote_dialect = ''
        if AI_API_KEY:
            try:
                generator = AIHometownGenerator(
                    api_key=AI_API_KEY,
                    base_url=AI_API_BASE_URL,
                    model=AI_MODEL
                )
                user_info = {
                    'hometown': user.hometown,
                    'current_city': getattr(user, 'current_city', ''),
                    'family_role': getattr(user, 'family_role', '妈妈'),
                    'nickname': getattr(user, 'nickname', '娃'),
                    'tone_style': getattr(user, 'tone_style', '唠叨型'),
                }
                ai_result = generator.generate_family_greeting(user_info)
                if ai_result:
                    quote_content = ai_result['content']
                    quote_dialect = ai_result.get('dialect', '')
                    # 保存 AI 问候记录
                    AIQuoteStorage.add_quote(
                        user.id,
                        quote_content,
                        user_info['family_role'],
                        quote_dialect
                    )
            except Exception as e:
                print(f"AI 生成失败：{e}")

        # 如果 AI 生成失败，使用内置话语
        if not quote_content:
            quote = QuoteGenerator.get_random_quote(user.id)
            quote_content = quote['content']

        # 创建签到记录
        checkin_data = {
            'checkin_date': datetime.now().strftime('%Y-%m-%d'),
            'checkin_time': datetime.now().isoformat(),
            'quote_content': quote_content
        }
        CheckinStorage.add_checkin(user.id, checkin_data)

        # 检查时间里程碑勋章
        days_away = user.get_days_away_from_home()
        time_badges = {
            1: 'day_1', 7: 'day_7', 30: 'day_30',
            100: 'day_100', 180: 'day_180', 365: 'day_365'
        }
        for threshold, badge_id in time_badges.items():
            if days_away == threshold:
                badge = BadgeStorage.add_badge(user.id, badge_id)
                if badge:
                    new_badges.append(BadgeStorage.get_definition(badge_id))

        # 检查连续签到勋章
        stats = user.get_checkin_stats()
        streak_badges = {
            3: 'streak_3', 7: 'streak_7', 15: 'streak_15',
            30: 'streak_30', 100: 'streak_100'
        }
        for threshold, badge_id in streak_badges.items():
            if stats['current_streak'] == threshold:
                badge = BadgeStorage.add_badge(user.id, badge_id)
                if badge:
                    new_badges.append(BadgeStorage.get_definition(badge_id))

        flash('签到成功！', 'success')
        return render_template(
            'checkin_result.html',
            user=user,
            quote={'content': quote_content, 'category': 'AI 生成' if AI_API_KEY else '内置', 'dialect': quote_dialect},
            new_badges=new_badges
        )

    # GET 请求显示签到页面
    if user.has_checked_in_today():
        flash('今天已经签到过了', 'info')
        return redirect(url_for('dashboard.index'))

    return render_template('checkin.html', user=user)


@checkin_bp.route('/checkin/history')
@login_required
def history():
    """签到历史"""
    user = User(UserStorage.get_by_id(session['user_id']))
    checkins = CheckinStorage.get_by_user(user.id)

    # 按时间倒序排列
    checkins = sorted(checkins, key=lambda x: x.get('checkin_time', ''), reverse=True)

    # 获取每条签到对应的话语（兼容新旧格式）
    for checkin in checkins:
        # 新格式：直接存储 quote_content
        if 'quote_content' in checkin:
            checkin['quote'] = {
                'content': checkin['quote_content'],
                'category': checkin.get('quote_category', 'AI 生成')
            }
        # 旧格式：存储 quote_id
        elif 'quote_id' in checkin:
            quote = QuoteGenerator.get_quote_by_id(checkin['quote_id'])
            checkin['quote'] = quote

    return render_template('checkin_history.html', user=user, checkins=checkins)
