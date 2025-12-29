from app import create_app, db
from app.models import Meal

app = create_app()

with app.app_context():
    meals = Meal.query.all()
    print('所有菜品及其图片状态:')
    for meal in meals:
        status = "有图片" if meal.image_url else "无图片"
        print(f'- {meal.name}: {status}')