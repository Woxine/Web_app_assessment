"""
应用配置文件
"""
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # 分页配置
    ITEMS_PER_PAGE = 12
    
    # 日志配置
    LOG_DIR = os.path.join(basedir, 'logs')
    LOG_FILE = 'app.log'
    LOG_MAX_BYTES = 10240000  # 10MB
    LOG_BACKUP_COUNT = 10


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    # 默认使用 SQLite，如需使用 MySQL 可通过环境变量 DATABASE_URL 设置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

