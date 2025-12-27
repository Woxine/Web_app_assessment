"""
用户认证相关路由
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm, ProfileEditForm
from app.utils import log_action

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        log_action(f"New user registered: {user.username} ({user.email})")
        flash('注册成功！请登录。', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # 尝试通过用户名或邮箱查找用户
        user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.username.data)
        ).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            log_action(f"User {user.username} logged in successfully")
            flash('登录成功！', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            log_action(f"Failed login attempt for: {form.username.data}")
            flash('用户名/邮箱或密码错误。', 'error')
    
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """用户登出"""
    username = current_user.username
    logout_user()
    log_action(f"User {username} logged out")
    flash('您已成功登出。', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile')
@login_required
def profile():
    """用户资料页面"""
    return render_template('profile.html', user=current_user)


@auth_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """编辑用户资料"""
    form = ProfileEditForm(original_username=current_user.username,
                          original_email=current_user.email)
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        
        log_action(f"User {current_user.username} updated profile")
        flash('资料已更新。', 'success')
        return redirect(url_for('auth.profile'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    return render_template('edit_profile.html', form=form)

