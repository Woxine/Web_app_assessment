"""
Flask-WTF 表单定义
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, \
    SelectField, RadioField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, \
    ValidationError, NumberRange, Optional
from app.models import User


class RegistrationForm(FlaskForm):
    """注册表单（包含至少5种控件）"""
    # 1. 文本输入框
    username = StringField('用户名', validators=[
        DataRequired(message='请输入用户名'),
        Length(min=3, max=20, message='用户名长度必须在3-20个字符之间')
    ])
    
    # 1. 文本输入框
    email = StringField('邮箱', validators=[
        DataRequired(message='请输入邮箱'),
        Email(message='请输入有效的邮箱地址')
    ])
    
    # 2. 密码输入框
    password = PasswordField('密码', validators=[
        DataRequired(message='请输入密码'),
        Length(min=8, message='密码长度至少为8个字符')
    ])
    
    # 2. 密码输入框
    password2 = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码'),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    
    # 6. 复选框
    agree_terms = BooleanField('我同意服务条款', validators=[
        DataRequired(message='请同意服务条款')
    ])
    
    # 3. 提交按钮
    submit = SubmitField('注册')
    
    def validate_username(self, username):
        """验证用户名唯一性"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该用户名已被使用，请选择其他用户名。')
    
    def validate_email(self, email):
        """验证邮箱唯一性"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('该邮箱已被注册，请使用其他邮箱。')
    
    def validate_password(self, password):
        """验证密码强度"""
        pwd = password.data
        if len(pwd) < 8:
            raise ValidationError('密码长度至少为8个字符。')
        if not any(c.isalpha() for c in pwd):
            raise ValidationError('密码必须包含至少一个字母。')
        if not any(c.isdigit() for c in pwd):
            raise ValidationError('密码必须包含至少一个数字。')


class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField('用户名或邮箱', validators=[
        DataRequired(message='请输入用户名或邮箱')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='请输入密码')
    ])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class SearchForm(FlaskForm):
    """搜索表单（包含多种控件）"""
    # 1. 文本输入框
    keyword = StringField('搜索关键词', validators=[
        DataRequired(message='请输入搜索关键词')
    ])
    
    # 5. 单选按钮
    search_type = RadioField('搜索类型', 
        choices=[('all', '全部'), ('crops', '作物'), ('meals', '菜品')],
        default='all',
        validators=[DataRequired()]
    )
    
    # 4. 下拉列表（多选项）
    sort_by = SelectField('排序方式',
        choices=[
            ('name', '按名称 (A-Z)'),
            ('hunger', '按恢复饱食度 (降序)'),
            ('likes', '按点赞数 (降序)')
        ],
        default='name',
        validators=[DataRequired()]
    )
    
    # 3. 提交按钮
    submit = SubmitField('搜索')


class ProfileEditForm(FlaskForm):
    """用户资料编辑表单"""
    username = StringField('用户名', validators=[
        DataRequired(),
        Length(min=3, max=20)
    ])
    email = StringField('邮箱', validators=[
        DataRequired(),
        Email()
    ])
    submit = SubmitField('保存更改')
    
    def __init__(self, original_username, original_email, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('该用户名已被使用。')
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('该邮箱已被注册。')


class CropForm(FlaskForm):
    """作物表单（用于 Flask-Admin 或手动添加）"""
    name = StringField('名称', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('描述')
    image_url = StringField('图片URL')
    hunger_points = IntegerField('恢复饱食度', validators=[NumberRange(min=0)])
    submit = SubmitField('提交')


class MealForm(FlaskForm):
    """菜品表单（用于 Flask-Admin 或手动添加）"""
    name = StringField('名称', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('描述')
    image_url = StringField('图片URL')
    hunger_restored = IntegerField('恢复饱食度', validators=[NumberRange(min=0)])
    saturation = FloatField('饱和度', validators=[NumberRange(min=0.0)])
    submit = SubmitField('提交')

