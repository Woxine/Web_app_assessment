"""
主视图路由
"""
from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import Crop, Meal, User
from app.forms import SearchForm
from flask_login import login_required, current_user
from sqlalchemy import func, or_

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """首页：展示模组简介和最受欢迎的3个菜品"""
    # 使用聚合查询获取最受欢迎的3个菜品（按点赞数）
    top_meals = (
        db.session.query(
            Meal,
            func.count(User.id).label('likes_count')
        )
        .join(Meal.liked_by_users)
        .group_by(Meal.id)
        .order_by(func.count(User.id).desc())
        .limit(3)
        .all()
    )

    # 如果没有点赞数据，则按创建时间降序获取3个菜品
    if not top_meals:
        top_meals = [
            (meal, 0) for meal in
            Meal.query.order_by(Meal.created_at.desc()).limit(3).all()
        ]

    return render_template('index.html', top_meals=top_meals)


@main_bp.route('/crops')
def crops():
    """作物列表页面（分页）"""
    page = request.args.get('page', 1, type=int)
    pagination = Crop.query.order_by(Crop.name.asc()).paginate(
        page=page, per_page=12, error_out=False
    )
    crops = pagination.items
    return render_template('crops.html', crops=crops, pagination=pagination)


@main_bp.route('/meals')
def meals():
    """菜品列表页面（分页）"""
    page = request.args.get('page', 1, type=int)
    pagination = Meal.query.order_by(Meal.name.asc()).paginate(
        page=page, per_page=12, error_out=False
    )
    meals = pagination.items
    return render_template('meals.html', meals=meals, pagination=pagination)


@main_bp.route('/crop/<int:id>')
def crop_detail(id):
    """作物详情页面"""
    crop = Crop.query.get_or_404(id)
    # 获取使用此作物的菜品
    related_meals = crop.meals.all()
    is_liked = False
    if current_user.is_authenticated:
        is_liked = crop in current_user.liked_crops.all()
    return render_template(
        'detail_crop.html',
        crop=crop,
        related_meals=related_meals,
        is_liked=is_liked
    )


@main_bp.route('/meal/<int:id>')
def meal_detail(id):
    """菜品详情页面"""
    meal = Meal.query.get_or_404(id)
    # 获取菜品所需的食材
    ingredients = meal.ingredients.all()
    is_liked = False
    if current_user.is_authenticated:
        is_liked = meal in current_user.liked_meals.all()
    return render_template(
        'detail_meal.html',
        meal=meal,
        ingredients=ingredients,
        is_liked=is_liked
    )


@main_bp.route('/search', methods=['GET', 'POST'])
def search():
    """搜索功能"""
    form = SearchForm()
    results = []

    if form.validate_on_submit():
        keyword = form.keyword.data
        search_type = form.search_type.data
        sort_by = form.sort_by.data

        # 构建查询
        if search_type == 'crops':
            query = Crop.query.filter(
                or_(
                    Crop.name.contains(keyword),
                    Crop.description.contains(keyword)
                )
            )
        elif search_type == 'meals':
            query = Meal.query.filter(
                or_(
                    Meal.name.contains(keyword),
                    Meal.description.contains(keyword)
                )
            )
        else:  # all
            # 搜索作物和菜品
            crops = Crop.query.filter(
                or_(
                    Crop.name.contains(keyword),
                    Crop.description.contains(keyword)
                )
            ).all()
            meals = Meal.query.filter(
                or_(
                    Meal.name.contains(keyword),
                    Meal.description.contains(keyword)
                )
            ).all()
            results = list(crops) + list(meals)

            # 排序
            if sort_by == 'name':
                results.sort(key=lambda x: x.name)
            elif sort_by == 'hunger':
                def get_hunger(item):
                    return getattr(
                        item, 'hunger_points',
                        getattr(item, 'hunger_restored', 0)
                    )
                results.sort(key=get_hunger, reverse=True)
            elif sort_by == 'likes':
                results.sort(
                    key=lambda x: x.get_likes_count(),
                    reverse=True
                )

            return render_template(
                'search.html',
                form=form,
                results=results,
                keyword=keyword
            )

        # 对单一类型进行排序
        if sort_by == 'name':
            query = query.order_by(
                Crop.name.asc() if search_type == 'crops' else Meal.name.asc()
            )
        elif sort_by == 'hunger':
            if search_type == 'crops':
                query = query.order_by(Crop.hunger_points.desc())
            else:
                query = query.order_by(Meal.hunger_restored.desc())
        elif sort_by == 'likes':
            # 需要聚合查询
            if search_type == 'crops':
                query = (
                    db.session.query(
                        Crop,
                        func.count(User.id).label('likes_count')
                    )
                    .join(Crop.liked_by_users, isouter=True)
                    .filter(
                        or_(
                            Crop.name.contains(keyword),
                            Crop.description.contains(keyword)
                        )
                    )
                    .group_by(Crop.id)
                    .order_by(func.count(User.id).desc())
                )
                results = [row[0] for row in query.all()]
            else:
                query = (
                    db.session.query(
                        Meal,
                        func.count(User.id).label('likes_count')
                    )
                    .join(Meal.liked_by_users, isouter=True)
                    .filter(
                        or_(
                            Meal.name.contains(keyword),
                            Meal.description.contains(keyword)
                        )
                    )
                    .group_by(Meal.id)
                    .order_by(func.count(User.id).desc())
                )
                results = [row[0] for row in query.all()]
            return render_template(
                'search.html',
                form=form,
                results=results,
                keyword=keyword
            )

        results = query.all()

    return render_template('search.html', form=form, results=results)


@main_bp.route('/rankings')
def rankings():
    """排行榜页面"""
    # 作物排行榜（按点赞数降序）
    crop_rankings = (
        db.session.query(
            Crop,
            func.count(User.id).label('likes_count')
        )
        .join(Crop.liked_by_users, isouter=True)
        .group_by(Crop.id)
        .order_by(func.count(User.id).desc())
        .limit(10)
        .all()
    )

    # 菜品排行榜（按点赞数降序）
    meal_rankings = (
        db.session.query(
            Meal,
            func.count(User.id).label('likes_count')
        )
        .join(Meal.liked_by_users, isouter=True)
        .group_by(Meal.id)
        .order_by(func.count(User.id).desc())
        .limit(10)
        .all()
    )

    return render_template(
        'rankings.html',
        crop_rankings=crop_rankings,
        meal_rankings=meal_rankings
    )


@main_bp.route('/api/like/crop/<int:id>', methods=['POST'])
@login_required
def like_crop(id):
    """AJAX 点赞作物"""
    crop = Crop.query.get_or_404(id)

    if crop in current_user.liked_crops.all():
        # 取消点赞
        current_user.liked_crops.remove(crop)
        is_liked = False
    else:
        # 添加点赞
        current_user.liked_crops.append(crop)
        is_liked = True

    db.session.commit()

    # 记录日志
    from app.utils import log_action
    action = "liked" if is_liked else "unliked"
    message = f"User {current_user.username} {action} crop {crop.name}"
    log_action(message)

    return jsonify({
        'success': True,
        'likes_count': crop.get_likes_count(),
        'is_liked': is_liked
    })


@main_bp.route('/api/like/meal/<int:id>', methods=['POST'])
@login_required
def like_meal(id):
    """AJAX 点赞菜品"""
    meal = Meal.query.get_or_404(id)

    if meal in current_user.liked_meals.all():
        # 取消点赞
        current_user.liked_meals.remove(meal)
        is_liked = False
    else:
        # 添加点赞
        current_user.liked_meals.append(meal)
        is_liked = True

    db.session.commit()

    # 记录日志
    from app.utils import log_action
    action = "liked" if is_liked else "unliked"
    message = f"User {current_user.username} {action} meal {meal.name}"
    log_action(message)

    return jsonify({
        'success': True,
        'likes_count': meal.get_likes_count(),
        'is_liked': is_liked
    })
