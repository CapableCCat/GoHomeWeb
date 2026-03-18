from flask import Flask, session
from flask_cors import CORS
from datetime import timedelta
from config import SECRET_KEY, DATABASE_URL, SQLALCHEMY_TRACK_MODIFICATIONS
from models.database import db, User, BUILTIN_QUOTES
from routes.auth import auth_bp
from routes.checkin import checkin_bp
from routes.dashboard import dashboard_bp
from routes.quotes import quotes_bp
from routes.ai_hometown import ai_hometown_bp
from routes.badges import badges_bp
import os


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    # 初始化数据库
    db.init_app(app)

    # 配置 CORS，允许前端跨域访问
    CORS(app, supports_credentials=True, origins=[
        'http://localhost:3000',
        'http://localhost:3001',
        'https://*.github.io'
    ])

    # 注册蓝图，统一使用 /api 前缀
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(checkin_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/api')
    app.register_blueprint(quotes_bp, url_prefix='/api')
    app.register_blueprint(ai_hometown_bp, url_prefix='/api')
    app.register_blueprint(badges_bp, url_prefix='/api')

    # 错误处理（改为 JSON 响应，适配前后端分离）
    @app.errorhandler(404)
    def not_found(error):
        return {'success': False, 'message': '接口不存在'}, 404

    @app.errorhandler(500)
    def server_error(error):
        return {'success': False, 'message': '服务器内部错误'}, 500

    return app


if __name__ == '__main__':
    app = create_app()

    # 确保数据目录存在
    from config import DATA_DIR
    os.makedirs(DATA_DIR, exist_ok=True)

    # 检查数据库是否需要初始化
    with app.app_context():
        from models.database import db, User
        if db.session.query(User).count() == 0:
            print("数据库为空，正在初始化...")
            from utils.db_init import initialize_data
            db.create_all()
            initialize_data()
            print("初始化完成!")

    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'

    app.run(debug=debug, host='0.0.0.0', port=port)
