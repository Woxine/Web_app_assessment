"""
Flask-Admin 配置
"""
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for, request
from wtforms import PasswordField
from app import db, admin
from app.models import User, Crop, Meal


class SecureAdminIndexView(AdminIndexView):
    """安全的管理后台首页视图"""
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        # 确保重定向到登录页面，并传递 next 参数
        return redirect(url_for('auth.login', next=request.url))


class SecureModelView(ModelView):
    """安全的基础模型视图"""
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == 'admin'
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))


class UserModelView(SecureModelView):
    """用户模型视图"""
    column_list = ['id', 'username', 'email', 'created_at']
    column_searchable_list = ['username', 'email']
    column_filters = ['created_at']
    form_excluded_columns = ['password_hash', 'liked_crops', 'liked_meals', 'created_at']
    
    # 添加密码字段到表单（用于创建/编辑用户）
    form_extra_fields = {
        'password': PasswordField('密码（留空则不修改）')
    }
    
    def on_model_change(self, form, model, is_created):
        """处理密码更新"""
        if form.password.data:
            model.set_password(form.password.data)


class CropModelView(SecureModelView):
    """作物模型视图"""
    column_list = ['id', 'name', 'hunger_points', 'created_at']
    column_searchable_list = ['name', 'description']
    column_filters = ['hunger_points', 'created_at']
    form_columns = ['name', 'description', 'image_url', 'hunger_points']
    # 允许批量删除
    can_delete = True
    can_export = True


class MealModelView(SecureModelView):
    """菜品模型视图"""
    column_list = ['id', 'name', 'hunger_restored', 'saturation', 'created_at']
    column_searchable_list = ['name', 'description']
    column_filters = ['hunger_restored', 'saturation', 'created_at']
    form_columns = ['name', 'description', 'image_url', 'hunger_restored', 'saturation', 'ingredients']
    # 允许批量删除
    can_delete = True
    can_export = True


def init_admin():
    """初始化 Flask-Admin"""
    # 设置模板模式为 Bootstrap 3（避免与我们的样式冲突）
    admin.template_mode = 'bootstrap3'
    admin.index_view = SecureAdminIndexView()
    admin.add_view(UserModelView(User, db.session, name='用户', endpoint='admin_users'))
    admin.add_view(CropModelView(Crop, db.session, name='作物', endpoint='admin_crops'))
    admin.add_view(MealModelView(Meal, db.session, name='菜品', endpoint='admin_meals'))

