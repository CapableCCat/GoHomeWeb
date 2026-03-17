"""API 端点集成测试"""
import json
import pytest
from app import create_app
from models.storage import UserStorage, CheckinStorage
from werkzeug.security import generate_password_hash
from datetime import datetime


@pytest.fixture
def app():
    """创建测试应用"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    yield app


@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()


@pytest.fixture
def test_user(app):
    """创建测试用户"""
    import time
    unique_username = f'testuser_{int(time.time() * 1000)}'
    with app.app_context():
        user_data = {
            'username': unique_username,
            'password_hash': generate_password_hash('password123'),
            'hometown': '湖南长沙',
            'current_city': '北京',
            'leave_home_date': '2026-01-01',
            'created_at': datetime.now().isoformat(),
            'family_role': '妈妈',
            'nickname': '娃',
            'tone_style': '唠叨型',
        }
        user = UserStorage.create(user_data)
        yield user
        # 清理 - 删除用户和签到数据
        with app.app_context():
            users = UserStorage.get_all()
            if str(user['id']) in users:
                del users[str(user['id'])]
                UserStorage.save_all(users)
            # 清理签到数据
            checkins = CheckinStorage.get_all()
            if str(user['id']) in checkins:
                del checkins[str(user['id'])]
                CheckinStorage.save_all(checkins)


class TestAuthAPI:
    """测试认证 API"""

    def test_login_success(self, client, test_user):
        """测试登录成功"""
        username = test_user['username']
        response = client.post(
            '/api/login',
            data=json.dumps({'username': username, 'password': 'password123'}),
            content_type='application/json'
        )
        data = response.get_json()
        assert response.status_code == 200
        assert data['success'] is True
        assert 'user' in data
        assert data['user']['username'] == username

    def test_login_wrong_password(self, client, test_user):
        """测试密码错误"""
        username = test_user['username']
        response = client.post(
            '/api/login',
            data=json.dumps({'username': username, 'password': 'wrongpassword'}),
            content_type='application/json'
        )
        data = response.get_json()
        assert response.status_code == 200
        assert data['success'] is False
        assert '用户名或密码错误' in data['message']

    def test_register_success(self, client):
        """测试注册成功"""
        import time
        unique_username = f'testuser_{int(time.time())}'
        response = client.post(
            '/api/register',
            data=json.dumps({
                'username': unique_username,
                'password': 'password123',
                'hometown': '上海',
                'current_city': '深圳',
                'family_role': '爸爸',
                'nickname': '小明',
                'tone_style': '幽默型'
            }),
            content_type='application/json'
        )
        data = response.get_json()
        assert response.status_code == 200
        assert data['success'] is True

        # 清理
        with client.application.app_context():
            user = UserStorage.get_by_username(unique_username)
            if user:
                users = UserStorage.get_all()
                if str(user['id']) in users:
                    del users[str(user['id'])]
                    UserStorage.save_all(users)

    def test_register_duplicate(self, client, test_user):
        """测试重复注册"""
        username = test_user['username']
        response = client.post(
            '/api/register',
            data=json.dumps({
                'username': username,
                'password': 'password123',
                'hometown': '湖南长沙',
                'current_city': '北京'
            }),
            content_type='application/json'
        )
        data = response.get_json()
        assert response.status_code == 200
        assert data['success'] is False
        assert '该用户名已被注册' in data['message']

    def test_logout(self, client, test_user):
        """测试登出"""
        username = test_user['username']
        # 先登录
        client.post(
            '/api/login',
            data=json.dumps({'username': username, 'password': 'password123'}),
            content_type='application/json'
        )
        # 再登出
        response = client.get('/api/logout')
        data = response.get_json()
        assert response.status_code == 200
        assert data['success'] is True


class TestProfileAPI:
    """测试用户资料 API"""

    def test_get_profile(self, client, test_user):
        """测试获取用户资料"""
        username = test_user['username']
        # 先登录
        client.post(
            '/api/login',
            data=json.dumps({'username': username, 'password': 'password123'}),
            content_type='application/json'
        )
        # 获取资料
        response = client.get('/api/profile')
        data = response.get_json()
        assert response.status_code == 200
        assert data['success'] is True
        assert data['user']['username'] == username
        assert data['user']['hometown'] == '湖南长沙'
        assert data['user']['family_role'] == '妈妈'

    def test_get_profile_unauthorized(self, client):
        """测试未授权访问"""
        response = client.get('/api/profile')
        # 未登录时会重定向到登录页
        assert response.status_code == 302

    def test_get_profile_unauthorized_json(self, client):
        """测试未授权访问（JSON 请求）"""
        response = client.get('/api/profile', headers={'Accept': 'application/json'})
        # 未登录时会重定向到登录页
        assert response.status_code == 302

    def test_update_profile(self, client, test_user):
        """测试更新用户资料"""
        username = test_user['username']
        # 先登录
        client.post(
            '/api/login',
            data=json.dumps({'username': username, 'password': 'password123'}),
            content_type='application/json'
        )
        # 更新资料
        response = client.put(
            '/api/profile',
            data=json.dumps({
                'hometown': '四川成都',
                'nickname': '宝贝'
            }),
            content_type='application/json'
        )
        data = response.get_json()
        assert response.status_code == 200
        assert data['success'] is True

        # 验证更新
        response = client.get('/api/profile')
        data = response.get_json()
        assert data['user']['hometown'] == '四川成都'
        assert data['user']['nickname'] == '宝贝'

    def test_get_profile_unauthorized(self, client):
        """测试未授权访问"""
        response = client.get('/api/profile')
        # 未登录时会重定向到登录页
        assert response.status_code == 302

    def test_get_profile_unauthorized_json(self, client):
        """测试未授权访问（JSON 请求）"""
        response = client.get('/api/profile', headers={'Accept': 'application/json'})
        # 未登录时会重定向到登录页
        assert response.status_code == 302


class TestCheckinAPI:
    """测试签到 API"""

    def test_do_checkin_duplicate(self, client, test_user):
        """测试重复签到"""
        username = test_user['username']
        # 先登录
        client.post(
            '/api/login',
            data=json.dumps({'username': username, 'password': 'password123'}),
            content_type='application/json'
        )
        # 第一次签到
        response = client.post('/api/checkin')
        data = response.get_json()
        assert data['success'] is True
        # 第二次签到
        response = client.post('/api/checkin')
        data = response.get_json()
        assert response.status_code == 200
        assert data['success'] is False
        assert '今天已经签到过了' in data['message']

    def test_do_checkin(self, client, test_user):
        """测试签到"""
        # test_user fixture 每次都会创建新用户，所以可以直接签到
        # 先登录
        username = test_user['username']
        client.post(
            '/api/login',
            data=json.dumps({'username': username, 'password': 'password123'}),
            content_type='application/json'
        )
        # 签到
        response = client.post('/api/checkin')
        data = response.get_json()
        assert response.status_code == 200
        assert data['success'] is True
        assert 'stats' in data
        assert 'checkin_date' in data

    def test_get_checkin_status(self, client, test_user):
        """测试获取签到状态"""
        username = test_user['username']
        # 先登录
        client.post(
            '/api/login',
            data=json.dumps({'username': username, 'password': 'password123'}),
            content_type='application/json'
        )
        # 获取状态
        response = client.get('/api/checkin/status')
        data = response.get_json()
        assert response.status_code == 200
        assert data['success'] is True
        assert 'has_checked_in_today' in data
        assert 'stats' in data

    def test_get_checkin_status_unauthorized(self, client):
        """测试未授权访问签到状态"""
        response = client.get('/api/checkin/status')
        # 未登录时会重定向到登录页
        assert response.status_code == 302
