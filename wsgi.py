"""
WSGI 配置文件（用于 PythonAnywhere 部署）
"""
import sys

# 添加项目路径到 Python 路径
path = '/home/yourusername/cw2'  # 修改为你的实际路径
if path not in sys.path:
    sys.path.insert(0, path)

from app import create_app

application = create_app('production')

if __name__ == "__main__":
    application.run()

