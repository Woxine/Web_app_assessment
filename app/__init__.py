"""
Farmer's Delight Wiki - Flask Application Factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin
from flask_migrate import Migrate
from flask_babel import Babel
import os

# 初始化扩展
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
admin = Admin(name="Farmer's Delight Wiki")
migrate = Migrate()
babel = Babel()


def create_app(config_name=None):
    """应用工厂函数"""
    app = Flask(__name__)

    # 配置
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    if config_name == 'production':
        app.config.from_object('config.ProductionConfig')
    elif config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    # 从实例文件夹加载配置（如果存在）
    instance_config_path = os.path.join(app.instance_path, 'config.py')
    if os.path.exists(instance_config_path):
        app.config.from_pyfile('config.py')

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    babel.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db)

    # 配置 Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    # 添加 CSRF token 到模板上下文
    @app.context_processor
    def inject_csrf_token():
        from flask_wtf.csrf import generate_csrf
        return dict(csrf_token=generate_csrf)

    # 注册蓝图
    from app.views import main_bp
    from app.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # 初始化 Flask-Admin
    from app.admin import init_admin
    init_admin()

    # 初始化日志
    from app.utils import init_logging
    init_logging(app)

    return app
