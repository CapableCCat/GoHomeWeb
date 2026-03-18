from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models.database import db, User
from models.storage import UserStorage

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册 API"""
    data = request.get_json()
    username = data.get('username', '').strip() if data else ''
    password = data.get('password', '') if data else ''
    hometown = data.get('hometown', '').strip() if data else ''
    current_city = data.get('current_city', '').strip() if data else ''
    leave_home_date = data.get('leave_home_date', '')
    family_role = data.get('family_role', '妈妈')
    nickname = data.get('nickname', '').strip()
    tone_style = data.get('tone_style', '唠叨型')

    # 验证输入
    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400

    if len(username) < 3:
        return jsonify({'success': False, 'message': '用户名至少需要 3 个字符'}), 400

    if len(password) < 6:
        return jsonify({'success': False, 'message': '密码至少需要 6 个字符'}), 400

    # 检查用户名是否已存在
    existing_user = db.session.execute(
        db.select(User).filter_by(username=username)
    ).first()

    if existing_user:
        return jsonify({'success': False, 'message': '该用户名已被注册'}), 400

    # 创建用户
    user = User(
        username=username,
        password_hash=generate_password_hash(password, method='pbkdf2:sha256'),
        hometown=hometown,
        current_city=current_city,
        leave_home_date=leave_home_date,
        family_role=family_role,
        nickname=nickname,
        tone_style=tone_style
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'success': True, 'user_id': user.id})


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录 API"""
    data = request.get_json()
    username = data.get('username', '').strip() if data else ''
    password = data.get('password', '') if data else ''

    # 验证输入
    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400

    # 查找用户
    user = db.session.execute(
        db.select(User).filter_by(username=username)
    ).first()

    if not user or not check_password_hash(user[0].password_hash, password):
        return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

    user = user[0]

    # 登录成功
    session['user_id'] = user.id
    session['username'] = user.username

    return jsonify({
        'success': True,
        'user': user.to_dict()
    })


@auth_bp.route('/logout', methods=['GET'])
def logout():
    """用户登出 API"""
    session.clear()
    return jsonify({'success': True, 'message': '已退出登录'})


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """获取当前登录用户信息"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '未登录'}), 401

    user = db.session.get(User, session['user_id'])
    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 404

    return jsonify({'success': True, 'user': user.to_dict()})


def login_required(f):
    """登录检查装饰器"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': '请先登录'}), 401
        return f(*args, **kwargs)
    return decorated_function
