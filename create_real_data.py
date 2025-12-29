"""
创建真实的 Farmer's Delight 数据
基于 Wiki 信息和常见游戏数据
"""
from app import create_app, db
from app.models import Crop, Meal

app = create_app()

# 真实的作物数据（基于 Farmer's Delight Wiki）
REAL_CROPS = [
    {
        'name': 'Cabbage',
        'description': 'Cabbage is a leafy vegetable crop that can be grown from cabbage seeds. It restores 1 hunger point when eaten raw.',
        'hunger_points': 1,
        'image_url': '/static/images/corps/Cabbage.jpg'  # 示例图片路径
    },
    {
        'name': 'Tomato',
        'description': 'Tomato is a red fruit crop that can be grown from tomato seeds. It restores 2 hunger points and can be used in various recipes.',
        'hunger_points': 2,
        'image_url': '/static/images/corps/Tomato.jpg'
    },
    {
        'name': 'Onion',
        'description': 'Onion is a bulbous vegetable that can be grown from onion seeds. It restores 1 hunger point and is commonly used as a cooking ingredient.',
        'hunger_points': 1,
        'image_url': '/static/images/corps/Onion.jpg'
    },
    {
        'name': 'Rice',
        'description': 'Rice is a grain crop that can be grown from rice seeds. It must be cooked before consumption and is a staple ingredient in many meals.',
        'hunger_points': 1,
        'image_url': '/static/images/corps/Rice.jpg'
    },
    {
        'name': 'Beetroot',
        'description': 'Beetroot is a root vegetable that can be grown from beetroot seeds. It restores 1 hunger point and has a deep red color.',
        'hunger_points': 1,
        'image_url': '/static/images/corps/Beetroot.jpg'
    },
    {
        'name': 'Carrot',
        'description': 'Carrot is an orange root vegetable that restores 3 hunger points. It can be eaten raw or used in various recipes.',
        'hunger_points': 3,
        'image_url': '/static/images/corps/Carrot.jpg'
    },
    {
        'name': 'Potato',
        'description': 'Potato is a starchy tuber that restores 1 hunger point when raw. It can be cooked in various ways to create delicious meals.',
        'hunger_points': 1,
        'image_url': '/static/images/corps/Potato.jpg'
    },
]

# 真实的菜品数据（基于 Farmer's Delight Wiki）
REAL_MEALS = [
    {
        'name': 'Noodle Soup',
        'description': 'A type of soup-based staple food where cooked noodles are soaked in a flavorful clear or thick broth.',
        'hunger_restored': 14,
        'saturation': 12.0,
        'ingredients': []  # 将在后面建立关系
    },
    {
        'name': 'Fried Rice',
        'description': 'A flavorful dish made with cooked rice, vegetables, and seasonings. A popular meal that restores 10 hunger points.',
        'hunger_restored': 10,
        'saturation': 8.0,
        'ingredients': ['Rice', 'Onion', 'Carrot']
    },
    {
        'name': 'Cooked Rice',
        'description': 'Simple cooked rice that restores 5 hunger points. A basic staple food.',
        'hunger_restored': 5,
        'saturation': 3.0,
        'ingredients': ['Rice']
    },
    {
        'name': 'Honey Glazed Ham',
        'description': 'A succulent ham glazed with honey. Restores 14 hunger points and provides excellent saturation.',
        'hunger_restored': 14,
        'saturation': 12.8,
        'ingredients': []
    },
    {
        'name': 'Smoked Ham',
        'description': 'A smoked ham that restores 12 hunger points. Rich in flavor and nutrition.',
        'hunger_restored': 12,
        'saturation': 10.4,
        'ingredients': []
    },
    {
        'name': 'Ham',
        'description': 'A basic ham that restores 8 hunger points. Can be used in various recipes.',
        'hunger_restored': 8,
        'saturation': 6.4,
        'ingredients': []
    },
    {
        'name': 'Tomato Soup',
        'description': 'A warm and comforting soup made from tomatoes. Restores 8 hunger points.',
        'hunger_restored': 8,
        'saturation': 6.0,
        'ingredients': ['Tomato', 'Onion']
    },
    {
        'name': 'Vegetable Salad',
        'description': 'A fresh and healthy salad made with various vegetables. Restores 6 hunger points.',
        'hunger_restored': 6,
        'saturation': 4.2,
        'ingredients': ['Cabbage', 'Tomato', 'Carrot']
    },
    {
        'name': 'Beetroot Soup',
        'description': 'A vibrant soup made from beetroot. Restores 7 hunger points and provides good nutrition.',
        'hunger_restored': 7,
        'saturation': 5.2,
        'ingredients': ['Beetroot', 'Onion']
    },
    {
        'name': 'Stuffed Pumpkin',
        'description': 'A pumpkin stuffed with various ingredients. Restores 12 hunger points and is a feast for special occasions.',
        'hunger_restored': 12,
        'saturation': 9.6,
        'ingredients': []
    },
]

def create_real_data():
    """创建真实数据"""
    with app.app_context():
        print("=" * 60)
        print("创建 Farmer's Delight 真实数据")
        print("=" * 60)
        
        # 创建作物
        print("\n步骤 1: 创建作物...")
        crops_dict = {}
        for crop_data in REAL_CROPS:
            existing = Crop.query.filter_by(name=crop_data['name']).first()
            if existing:
                print(f"  - 作物 {crop_data['name']} 已存在，跳过")
                crops_dict[crop_data['name']] = existing
            else:
                crop = Crop(
                    name=crop_data['name'],
                    description=crop_data['description'],
                    hunger_points=crop_data['hunger_points'],
                    image_url=crop_data.get('image_url', '')
                )
                db.session.add(crop)
                crops_dict[crop_data['name']] = crop
                print(f"  ✓ 创建作物: {crop_data['name']}")
        
        db.session.commit()
        
        # 创建菜品
        print("\n步骤 2: 创建菜品...")
        meals_dict = {}
        for meal_data in REAL_MEALS:
            existing = Meal.query.filter_by(name=meal_data['name']).first()
            if existing:
                print(f"  - 菜品 {meal_data['name']} 已存在，跳过")
                meals_dict[meal_data['name']] = existing
            else:
                meal = Meal(
                    name=meal_data['name'],
                    description=meal_data['description'],
                    hunger_restored=meal_data['hunger_restored'],
                    saturation=meal_data['saturation'],
                    image_url=meal_data.get('image_url', '')
                )
                db.session.add(meal)
                meals_dict[meal_data['name']] = meal
                print(f"  ✓ 创建菜品: {meal_data['name']}")
        
        db.session.commit()
        
        # 建立菜品-食材关系
        print("\n步骤 3: 建立菜品-食材关系...")
        relationships_count = 0
        for meal_data in REAL_MEALS:
            meal = meals_dict.get(meal_data['name'])
            if not meal:
                continue
            
            for ing_name in meal_data.get('ingredients', []):
                crop = crops_dict.get(ing_name)
                if crop and crop not in meal.ingredients.all():
                    meal.ingredients.append(crop)
                    relationships_count += 1
                    print(f"  ✓ {meal_data['name']} ← {ing_name}")
        
        db.session.commit()
        
        print("\n" + "=" * 60)
        print(f"数据创建完成！")
        print(f"  - 作物: {len(crops_dict)} 个")
        print(f"  - 菜品: {len(meals_dict)} 个")
        print(f"  - 关系: {relationships_count} 个")
        print("=" * 60)

if __name__ == '__main__':
    create_real_data()

