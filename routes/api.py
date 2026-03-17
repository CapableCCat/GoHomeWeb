from flask import Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models.storage import UserStorage
from models.user import User
from models.badge import BadgeStorage
from models.ai_quote import AIQuoteStorage
from routes.auth import login_required

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/login', methods=['POST'])
def login():
    """登录 API"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'})

    user_data = UserStorage.get_by_username(username)
    if not user_data or not check_password_hash(user_data.get('password_hash', ''), password):
        return jsonify({'success': False, 'message': '用户名或密码错误'})

    session['user_id'] = user_data['id']
    session['username'] = user_data['username']

    user = User(user_data)
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'hometown': user.hometown,
            'current_city': user.current_city,
            'family_role': getattr(user, 'family_role', '妈妈'),
            'nickname': getattr(user, 'nickname', ''),
            'tone_style': getattr(user, 'tone_style', '唠叨型')
        }
    })


@api_bp.route('/register', methods=['POST'])
def register():
    """注册 API"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    hometown = data.get('hometown', '').strip()
    current_city = data.get('current_city', '').strip()
    leave_home_date = data.get('leave_home_date', '')
    family_role = data.get('family_role', '妈妈')
    nickname = data.get('nickname', '').strip()
    tone_style = data.get('tone_style', '唠叨型')

    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'})

    if len(username) < 3:
        return jsonify({'success': False, 'message': '用户名至少需要 3 个字符'})

    if len(password) < 6:
        return jsonify({'success': False, 'message': '密码至少需要 6 个字符'})

    existing_user = UserStorage.get_by_username(username)
    if existing_user:
        return jsonify({'success': False, 'message': '该用户名已被注册'})

    user_data = {
        'username': username,
        'password_hash': generate_password_hash(password),
        'hometown': hometown,
        'current_city': current_city,
        'leave_home_date': leave_home_date,
        'created_at': datetime.now().isoformat(),
        'family_role': family_role,
        'nickname': nickname,
        'tone_style': tone_style,
    }
    created_user = UserStorage.create(user_data)

    return jsonify({'success': True})


@api_bp.route('/logout', methods=['GET'])
def logout():
    """登出 API"""
    session.clear()
    return jsonify({'success': True})


@api_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """获取用户资料 API"""
    user_data = UserStorage.get_by_id(session['user_id'])
    if not user_data:
        return jsonify({'success': False, 'message': '用户不存在'})

    user = User(user_data)
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'hometown': user.hometown,
            'current_city': user.current_city,
            'leave_home_date': user.leave_home_date,
            'family_role': getattr(user, 'family_role', '妈妈'),
            'nickname': getattr(user, 'nickname', ''),
            'tone_style': getattr(user, 'tone_style', '唠叨型')
        }
    })


@api_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """更新用户资料 API"""
    data = request.get_json()
    user_data = UserStorage.get_by_id(session['user_id'])
    if not user_data:
        return jsonify({'success': False, 'message': '用户不存在'})

    # 更新字段
    if 'hometown' in data:
        user_data['hometown'] = data['hometown']
    if 'current_city' in data:
        user_data['current_city'] = data['current_city']
    if 'leave_home_date' in data:
        user_data['leave_home_date'] = data['leave_home_date']
    if 'family_role' in data:
        user_data['family_role'] = data['family_role']
    if 'nickname' in data:
        user_data['nickname'] = data['nickname']
    if 'tone_style' in data:
        user_data['tone_style'] = data['tone_style']

    UserStorage.update(session['user_id'], user_data)
    return jsonify({'success': True})


@api_bp.route('/checkin', methods=['POST'])
@login_required
def do_checkin():
    """签到 API"""
    from routes.checkin import do_checkin as checkin_action
    user = User(UserStorage.get_by_id(session['user_id']))

    # 检查今天是否已经签到
    today = datetime.now().strftime('%Y-%m-%d')
    if user.has_checked_in_today():
        return jsonify({
            'success': False,
            'message': '今天已经签到过了'
        })

    # 执行签到
    checkin_data = {
        'checkin_date': today,
        'checkin_time': datetime.now().isoformat()
    }
    from models.storage import CheckinStorage
    CheckinStorage.add_checkin(user.id, checkin_data)

    new_badges = []

    # 检查特殊成就勋章
    checkin_time = datetime.now()
    if checkin_time.hour >= 2:
        badge = BadgeStorage.add_badge(user.id, 'late_night')
        if badge:
            new_badges.append(BadgeStorage.get_definition('late_night'))
    elif checkin_time.hour < 6:
        badge = BadgeStorage.add_badge(user.id, 'early_bird')
        if badge:
            new_badges.append(BadgeStorage.get_definition('early_bird'))

    # AI 生成家人问候
    quote_content = None
    from utils.ai_hometown_generator import AIHometownGenerator
    import os
    AI_API_KEY = os.environ.get('AI_API_KEY')

    if AI_API_KEY:
        generator = AIHometownGenerator(AI_API_KEY)
        user_info = {
            'hometown': user.hometown,
            'family_role': getattr(user, 'family_role', '妈妈'),
            'nickname': getattr(user, 'nickname', '娃'),
            'tone_style': getattr(user, 'tone_style', '唠叨型'),
        }
        ai_result = generator.generate_family_greeting(user_info)
        if ai_result:
            quote_content = ai_result['content']
            AIQuoteStorage.add_quote(
                user.id,
                quote_content,
                user_info['family_role'],
                ai_result.get('dialect', '')
            )

    # 检查时间里程碑勋章
    days_away = user.get_days_away_from_home()
    time_badges = {1: 'day_1', 7: 'day_7', 30: 'day_30', 100: 'day_100', 180: 'day_180', 365: 'day_365'}
    for threshold, badge_id in time_badges.items():
        if days_away == threshold:
            badge = BadgeStorage.add_badge(user.id, badge_id)
            if badge:
                new_badges.append(BadgeStorage.get_definition(badge_id))

    # 检查连续签到勋章
    stats = user.get_checkin_stats()
    streak_badges = {3: 'streak_3', 7: 'streak_7', 15: 'streak_15', 30: 'streak_30', 100: 'streak_100'}
    for threshold, badge_id in streak_badges.items():
        if stats['current_streak'] == threshold:
            badge = BadgeStorage.add_badge(user.id, badge_id)
            if badge:
                new_badges.append(BadgeStorage.get_definition(badge_id))

    # 返回结果
    result = {
        'success': True,
        'checkin_date': today,
        'stats': stats,
        'new_badges': new_badges
    }

    if quote_content:
        result['quote'] = {
            'content': quote_content,
            'family_role': getattr(user, 'family_role', '妈妈'),
            'dialect': getattr(user, 'hometown', '')
        }

    return jsonify(result)


@api_bp.route('/checkin/status', methods=['GET'])
@login_required
def checkin_status():
    """获取签到状态 API"""
    user = User(UserStorage.get_by_id(session['user_id']))
    stats = user.get_checkin_stats()

    return jsonify({
        'success': True,
        'has_checked_in_today': user.has_checked_in_today(),
        'stats': stats,
        'last_checkin': {
            'checkin_date': stats.get('last_checkin_date', '')
        } if stats.get('last_checkin_date') else None
    })


@api_bp.route('/checkin/history', methods=['GET'])
@login_required
def checkin_history():
    """获取签到历史 API"""
    from models.storage import CheckinStorage
    checkins = CheckinStorage.get_user_checkins(session['user_id'])
    return jsonify({
        'success': True,
        'checkins': checkins
    })
