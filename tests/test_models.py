"""
数据库模型测试
"""
import unittest
from app import create_app, db
from app.models import User, Crop, Meal


class ModelTestCase(unittest.TestCase):
    """模型测试用例"""
    
    def setUp(self):
        """测试前准备"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """测试后清理"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_user_creation(self):
        """测试用户创建"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.check_password('wrongpassword'))
    
    def test_crop_creation(self):
        """测试作物创建"""
        crop = Crop(name='测试作物', description='这是一个测试作物', hunger_points=2)
        db.session.add(crop)
        db.session.commit()
        
        self.assertIsNotNone(crop.id)
        self.assertEqual(crop.name, '测试作物')
        self.assertEqual(crop.get_likes_count(), 0)
    
    def test_meal_creation(self):
        """测试菜品创建"""
        meal = Meal(name='测试菜品', description='这是一个测试菜品', 
                   hunger_restored=10, saturation=5.0)
        db.session.add(meal)
        db.session.commit()
        
        self.assertIsNotNone(meal.id)
        self.assertEqual(meal.name, '测试菜品')
        self.assertEqual(meal.get_likes_count(), 0)
    
    def test_user_like_crop(self):
        """测试用户点赞作物（多对多关系）"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        crop = Crop(name='测试作物', hunger_points=2)
        
        db.session.add(user)
        db.session.add(crop)
        db.session.commit()
        
        user.liked_crops.append(crop)
        db.session.commit()
        
        self.assertEqual(user.liked_crops.count(), 1)
        self.assertEqual(crop.liked_by_users.count(), 1)
        self.assertEqual(crop.get_likes_count(), 1)
    
    def test_user_like_meal(self):
        """测试用户点赞菜品（多对多关系）"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        meal = Meal(name='测试菜品', hunger_restored=10)
        
        db.session.add(user)
        db.session.add(meal)
        db.session.commit()
        
        user.liked_meals.append(meal)
        db.session.commit()
        
        self.assertEqual(user.liked_meals.count(), 1)
        self.assertEqual(meal.liked_by_users.count(), 1)
        self.assertEqual(meal.get_likes_count(), 1)
    
    def test_meal_ingredients_relationship(self):
        """测试菜品-食材关系（多对多）"""
        crop1 = Crop(name='作物1', hunger_points=1)
        crop2 = Crop(name='作物2', hunger_points=1)
        meal = Meal(name='测试菜品', hunger_restored=10)
        
        db.session.add(crop1)
        db.session.add(crop2)
        db.session.add(meal)
        db.session.commit()
        
        meal.ingredients.append(crop1)
        meal.ingredients.append(crop2)
        db.session.commit()
        
        self.assertEqual(meal.ingredients.count(), 2)
        self.assertIn(crop1, meal.ingredients.all())
        self.assertIn(crop2, meal.ingredients.all())


if __name__ == '__main__':
    unittest.main()

