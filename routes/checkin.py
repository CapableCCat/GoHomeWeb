from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from datetime import datetime
from models.user import User
from models.storage import CheckinStorage, QuoteStorage, UserStorage
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
        # 检查今天是否已签到
        if user.has_checked_in_today():
            flash('今天已经签到过了', 'info')
            return redirect(url_for('dashboard.index'))

        # 优先尝试 AI 生成思乡话语（如果配置了 API）
        quote_content = None
        if AI_API_KEY:
            try:
                generator = AIHometownGenerator(
                    api_key=AI_API_KEY,
                    base_url=AI_API_BASE_URL,
                    model=AI_MODEL
                )
                user_info = {
                    'hometown': user.hometown,
                    'current_city': getattr(user, 'current_city', '')
                }
                ai_result = generator.generate_for_checkin(user_info)
                if ai_result:
                    quote_content = ai_result['content']
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

        flash('签到成功！', 'success')
        return render_template('checkin_result.html', user=user, quote={'content': quote_content, 'category': 'AI 生成' if AI_API_KEY else '内置'})

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
