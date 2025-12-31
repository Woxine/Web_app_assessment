"""
Update Meal Image URLs
"""
from app import create_app, db
from app.models import Meal

app = create_app()

# Mapping of meal names to image files
MEAL_IMAGE_MAPPING = {
    'Beetroot Soup': 'Beetroot_Soup.png',
    'Cooked Rice': 'Cooked_Rice.webp',
    'Fried Rice': 'Fried_Rice.webp',
    'Ham': 'Ham.webp',
    'Smoked Ham': 'Smoked_Ham.webp',
    'Stuffed Pumpkin': 'Stuffed_Pumpkin_Block.webp',
    'Tomato Soup': 'Tomato_Sauce.webp',
    'Vegetable Salad': 'Mixed_Salad.webp',
    'Noodle Soup': 'Noodle_Soup.webp',
    'Honey Glazed Ham': 'Honey_Glazed_Ham_Block.webp',
}

def update_meal_images():
    """Update Meal Image URLs"""
    with app.app_context():
        print("=" * 60)
        print("Update Meal Image URLs")
        print("=" * 60)

        updated_count = 0
        for meal_name, image_file in MEAL_IMAGE_MAPPING.items():
            meal = Meal.query.filter_by(name=meal_name).first()
            if meal:
                if image_file:
                    image_url = f'/static/images/meal/{image_file}'
                    meal.image_url = image_url
                    print(f"  ✓ 更新 {meal_name} → {image_url}")
                    updated_count += 1
                else:
                    print(f"  - {meal_name} 暂无图片")
            else:
                print(f"  ✗ 未找到菜品: {meal_name}")

        db.session.commit()
        print("\n" + "=" * 60)
        print(f"更新完成！共更新 {updated_count} 个菜品的图片")
        print("=" * 60)

if __name__ == '__main__':
    update_meal_images()