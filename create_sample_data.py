"""
创建示例数据脚本
"""
from app import create_app, db
from app.models import User, Crop, Meal

app = create_app()

with app.app_context():
    # 清空现有数据（可选）
    # db.drop_all()
    # db.create_all()
    
    # 创建管理员用户
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('admin123')
        db.session.add(admin)
        print("创建管理员用户: admin / admin123")
    
    # 创建示例作物
    crops_data = [
        {'name': '番茄', 'description': '红色的圆形蔬菜，可以生吃或烹饪', 'hunger_points': 2},
        {'name': '胡萝卜', 'description': '橙色的根茎类蔬菜，营养丰富', 'hunger_points': 3},
        {'name': '土豆', 'description': '淀粉含量高的块茎类蔬菜', 'hunger_points': 1},
        {'name': '洋葱', 'description': '具有独特香味的球茎类蔬菜', 'hunger_points': 2},
        {'name': '卷心菜', 'description': '绿色的叶菜类蔬菜', 'hunger_points': 1},
        {'name': '甜菜根', 'description': '深红色的根茎类蔬菜', 'hunger_points': 2},
    ]
    
    for crop_data in crops_data:
        crop = Crop.query.filter_by(name=crop_data['name']).first()
        if not crop:
            crop = Crop(**crop_data)
            db.session.add(crop)
            print(f"创建作物: {crop_data['name']}")
    
    # 创建示例菜品
    meals_data = [
        {
            'name': '番茄汤',
            'description': '用新鲜番茄制作的温暖汤品',
            'hunger_restored': 8,
            'saturation': 6.0
        },
        {
            'name': '胡萝卜蛋糕',
            'description': '香甜可口的胡萝卜蛋糕',
            'hunger_restored': 10,
            'saturation': 8.0
        },
        {
            'name': '烤土豆',
            'description': '简单美味的烤土豆',
            'hunger_restored': 6,
            'saturation': 4.0
        },
        {
            'name': '蔬菜沙拉',
            'description': '新鲜蔬菜制作的健康沙拉',
            'hunger_restored': 5,
            'saturation': 3.0
        },
    ]
    
    for meal_data in meals_data:
        meal = Meal.query.filter_by(name=meal_data['name']).first()
        if not meal:
            meal = Meal(**meal_data)
            db.session.add(meal)
            print(f"创建菜品: {meal_data['name']}")
    
    # 提交更改
    db.session.commit()
    
    # 建立菜品-食材关系
    tomato = Crop.query.filter_by(name='番茄').first()
    carrot = Crop.query.filter_by(name='胡萝卜').first()
    potato = Crop.query.filter_by(name='土豆').first()
    onion = Crop.query.filter_by(name='洋葱').first()
    cabbage = Crop.query.filter_by(name='卷心菜').first()
    
    tomato_soup = Meal.query.filter_by(name='番茄汤').first()
    carrot_cake = Meal.query.filter_by(name='胡萝卜蛋糕').first()
    baked_potato = Meal.query.filter_by(name='烤土豆').first()
    salad = Meal.query.filter_by(name='蔬菜沙拉').first()
    
    if tomato and tomato_soup:
        if tomato not in tomato_soup.ingredients.all():
            tomato_soup.ingredients.append(tomato)
            tomato_soup.ingredients.append(onion)
            print("建立关系: 番茄汤 ← 番茄, 洋葱")
    
    if carrot and carrot_cake:
        if carrot not in carrot_cake.ingredients.all():
            carrot_cake.ingredients.append(carrot)
            print("建立关系: 胡萝卜蛋糕 ← 胡萝卜")
    
    if potato and baked_potato:
        if potato not in baked_potato.ingredients.all():
            baked_potato.ingredients.append(potato)
            print("建立关系: 烤土豆 ← 土豆")
    
    if salad:
        if cabbage and cabbage not in salad.ingredients.all():
            salad.ingredients.append(cabbage)
        if carrot and carrot not in salad.ingredients.all():
            salad.ingredients.append(carrot)
        if tomato and tomato not in salad.ingredients.all():
            salad.ingredients.append(tomato)
        print("建立关系: 蔬菜沙拉 ← 卷心菜, 胡萝卜, 番茄")
    
    db.session.commit()
    print("\n示例数据创建完成！")

