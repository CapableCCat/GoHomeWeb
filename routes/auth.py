from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models.storage import UserStorage
from models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    """首页"""
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))
    return render_template('index.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        hometown = request.form.get('hometown', '').strip()
        current_city = request.form.get('current_city', '').strip()
        leave_home_date = request.form.get('leave_home_date', '')
        # 家人配置
        family_role = request.form.get('family_role', '妈妈')
        nickname = request.form.get('nickname', '').strip()
        tone_style = request.form.get('tone_style', '唠叨型')

        # 验证输入
        if not username or not password:
            flash('用户名和密码不能为空', 'error')
            return render_template('register.html')

        if len(username) < 3:
            flash('用户名至少需要 3 个字符', 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash('密码至少需要 6 个字符', 'error')
            return render_template('register.html')

        # 检查用户名是否已存在
        existing_user = UserStorage.get_by_username(username)
        if existing_user:
            flash('该用户名已被注册', 'error')
            return render_template('register.html')

        # 创建用户
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

        flash('注册成功，请登录', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)

        # 验证输入
        if not username or not password:
            flash('用户名和密码不能为空', 'error')
            return render_template('login.html')

        # 查找用户
        user_data = UserStorage.get_by_username(username)
        if not user_data or not check_password_hash(user_data.get('password_hash', ''), password):
            flash('用户名或密码错误', 'error')
            return render_template('login.html')

        # 登录成功
        session['user_id'] = user_data['id']
        session['username'] = user_data['username']

        if remember:
            session.permanent = True

        flash('登录成功', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """用户登出"""
    session.clear()
    flash('已退出登录', 'info')
    return redirect(url_for('auth.index'))


def login_required(f):
    """登录检查装饰器"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
