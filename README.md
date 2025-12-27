# Farmer's Delight Wiki

基于 Flask 的 Minecraft 模组 "Farmer's Delight" 百科类 Web 应用。

## 功能特性

- ✅ 作物和菜品信息浏览（分页展示）
- ✅ 搜索功能（支持关键词检索和多种排序方式）
- ✅ 用户注册/登录系统（密码加密）
- ✅ AJAX 点赞功能（无刷新交互）
- ✅ 排行榜（基于点赞数）
- ✅ Flask-Admin 后台管理
- ✅ 响应式设计（WCAG 兼容）
- ✅ 安全措施（SQL 注入、XSS、CSRF 防护）
- ✅ 日志记录系统

## 技术栈

- **后端**: Python 3 + Flask
- **数据库**: Flask-SQLAlchemy (SQLite/MySQL)
- **前端**: Jinja2 + HTML5 + CSS3
- **表单**: Flask-WTF (CSRF 保护)
- **认证**: Flask-Login
- **管理**: Flask-Admin
- **迁移**: Flask-Migrate

## 安装步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd cw2
```

### 2. 创建虚拟环境

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

创建 `instance/config.py` 文件：

```python
SECRET_KEY = 'your-secret-key-here'
DATABASE_URL = 'sqlite:///app.db'  # 开发环境
# 或
# DATABASE_URL = 'mysql://user:password@localhost/farmers_delight'  # 生产环境
```

### 5. 初始化数据库

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. 运行应用

```bash
python run.py
```

访问 http://localhost:5000

## 数据库模型

### 核心模型

- **User**: 用户表（id, username, email, password_hash）
- **Crop**: 作物表（id, name, description, image_url, hunger_points）
- **Meal**: 菜品表（id, name, description, image_url, hunger_restored, saturation）

### 多对多关系

1. **meal_ingredients**: Meal ↔ Crop（菜品-食材关系）
2. **user_likes_crops**: User ↔ Crop（用户点赞作物）
3. **user_likes_meals**: User ↔ Meal（用户点赞菜品）

## 表单控件类型

满足至少 5 种表单控件要求：

1. 文本输入框 (TextInput)
2. 密码输入框 (PasswordField)
3. 提交按钮 (SubmitField)
4. 下拉列表 (SelectField)
5. 单选按钮 (RadioField)
6. 复选框 (BooleanField)
7. 文本域 (TextAreaField)

## 运行测试

```bash
python -m pytest tests/
# 或
python -m unittest discover tests
```

## 部署到 PythonAnywhere

1. 上传项目文件到 PythonAnywhere
2. 配置 WSGI 文件（参考 `wsgi.py`）
3. 设置环境变量（SECRET_KEY, DATABASE_URL）
4. 运行数据库迁移
5. 配置静态文件路径

## 安全措施

- ✅ SQL 注入防护：使用 SQLAlchemy ORM
- ✅ XSS 防护：Jinja2 自动转义
- ✅ CSRF 防护：Flask-WTF CSRF Token
- ✅ 密码加密：Werkzeug security

## 可访问性

- ✅ 语义化 HTML5（nav, main, article, footer）
- ✅ ARIA 标签（aria-label, aria-describedby）
- ✅ 颜色对比度符合 WCAG AA 级标准

## 项目结构

```
cw2/
├── app/
│   ├── __init__.py          # Flask 应用工厂
│   ├── models.py            # 数据模型
│   ├── forms.py             # Flask-WTF 表单
│   ├── views.py             # 主视图路由
│   ├── auth.py              # 认证路由
│   ├── admin.py             # Flask-Admin 配置
│   ├── utils.py             # 工具函数
│   ├── static/              # 静态文件
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/           # Jinja2 模板
├── tests/                   # 单元测试
├── migrations/              # 数据库迁移
├── instance/                # 实例配置
├── logs/                    # 日志文件
├── config.py                # 配置文件
├── run.py                   # 应用入口
├── wsgi.py                  # WSGI 配置
└── requirements.txt         # 依赖列表
```

## 许可证

本项目为课程作业项目。

## 作者

Leeds University - XJCO2011 Web Application Development

