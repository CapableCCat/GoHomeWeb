from flask import Flask, session, render_template
from datetime import timedelta
from config import SECRET_KEY
from routes.auth import auth_bp
from routes.checkin import checkin_bp
from routes.dashboard import dashboard_bp
from routes.quotes import quotes_bp
from routes.ai_hometown import ai_hometown_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(checkin_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(quotes_bp)
    app.register_blueprint(ai_hometown_bp)

    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html', message='页面不存在'), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template('error.html', message='服务器错误'), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
