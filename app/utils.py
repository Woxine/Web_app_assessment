"""
工具函数
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from flask import current_app


def init_logging(app):
    """初始化日志系统"""
    if not os.path.exists(app.config['LOG_DIR']):
        os.makedirs(app.config['LOG_DIR'])

    log_file = os.path.join(app.config['LOG_DIR'], app.config['LOG_FILE'])

    # 配置日志格式
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )

    # 文件处理器（轮转）
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=app.config['LOG_MAX_BYTES'],
        backupCount=app.config['LOG_BACKUP_COUNT']
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Farmer\'s Delight Wiki startup')


def log_action(message):
    """记录用户操作"""
    current_app.logger.info(f'ACTION: {message}')
