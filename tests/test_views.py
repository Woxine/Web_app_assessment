"""
视图路由测试
"""
import unittest
from app import create_app, db
from app.models import User, Crop, Meal


class ViewTestCase(unittest.TestCase):
    """视图测试用例"""
    
    def setUp(self):
        """测试前准备"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
    
    def tearDown(self):
        """测试后清理"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_index_page(self):
        """测试首页"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Farmer\'s Delight', response.data)
    
    def test_crops_page(self):
        """测试作物列表页"""
        response = self.client.get('/crops')
        self.assertEqual(response.status_code, 200)
    
    def test_meals_page(self):
        """测试菜品列表页"""
        response = self.client.get('/meals')
        self.assertEqual(response.status_code, 200)
    
    def test_crop_detail(self):
        """测试作物详情页"""
        crop = Crop(name='测试作物', hunger_points=2)
        db.session.add(crop)
        db.session.commit()
        
        response = self.client.get(f'/crop/{crop.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'测试作物', response.data)
    
    def test_meal_detail(self):
        """测试菜品详情页"""
        meal = Meal(name='测试菜品', hunger_restored=10)
        db.session.add(meal)
        db.session.commit()
        
        response = self.client.get(f'/meal/{meal.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'测试菜品', response.data)
    
    def test_search_page(self):
        """测试搜索页"""
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 200)
    
    def test_rankings_page(self):
        """测试排行榜页"""
        response = self.client.get('/rankings')
        self.assertEqual(response.status_code, 200)
    
    def test_like_crop_requires_login(self):
        """测试点赞需要登录"""
        crop = Crop(name='测试作物', hunger_points=2)
        db.session.add(crop)
        db.session.commit()
        
        response = self.client.post(f'/api/like/crop/{crop.id}')
        # 应该重定向到登录页或返回 401
        self.assertIn(response.status_code, [302, 401])


if __name__ == '__main__':
    unittest.main()

