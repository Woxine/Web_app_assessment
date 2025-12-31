"""
数据库模型定义
"""
from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# 关联表：菜品-食材（多对多）
meal_ingredients = db.Table(
    'meal_ingredients',
    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id'), primary_key=True),
    db.Column('crop_id', db.Integer, db.ForeignKey('crop.id'), primary_key=True),
    db.Column('quantity', db.Integer, default=1, nullable=False)
)

# 关联表：用户-作物点赞（多对多）
user_likes_crops = db.Table(
    'user_likes_crops',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('crop_id', db.Integer, db.ForeignKey('crop.id'), primary_key=True),
    db.Column('liked_at', db.DateTime, default=datetime.utcnow, nullable=False)
)

# 关联表：用户-菜品点赞（多对多）
user_likes_meals = db.Table(
    'user_likes_meals',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('meal_id', db.Integer, db.ForeignKey('meal.id'), primary_key=True),
    db.Column('liked_at', db.DateTime, default=datetime.utcnow, nullable=False)
)


class User(UserMixin, db.Model):
    """用户模型"""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # 多对多关系：用户点赞的作物
    liked_crops = db.relationship(
        'Crop', secondary=user_likes_crops,
        backref=db.backref('liked_by_users', lazy='dynamic'),
        lazy='dynamic'
    )

    # 多对多关系：用户点赞的菜品
    liked_meals = db.relationship(
        'Meal', secondary=user_likes_meals,
        backref=db.backref('liked_by_users', lazy='dynamic'),
        lazy='dynamic'
    )

    def set_password(self, password):
        """设置密码（加密）"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Crop(db.Model):
    """作物模型"""
    __tablename__ = 'crop'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    hunger_points = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # 多对多关系：使用此作物的菜品（通过 meal_ingredients）
    meals = db.relationship(
        'Meal', secondary=meal_ingredients,
        backref=db.backref('ingredients', lazy='dynamic'),
        lazy='dynamic'
    )

    def get_likes_count(self):
        """获取点赞数"""
        return self.liked_by_users.count()

    def __repr__(self):
        return f'<Crop {self.name}>'


class Meal(db.Model):
    """菜品模型"""
    __tablename__ = 'meal'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    hunger_restored = db.Column(db.Integer, default=0, nullable=False)
    saturation = db.Column(db.Float, default=0.0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def get_likes_count(self):
        """获取点赞数"""
        return self.liked_by_users.count()

    def __repr__(self):
        return f'<Meal {self.name}>'
