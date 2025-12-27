"""
认证功能测试
"""
import unittest
from app import create_app, db
from app.models import User


class AuthTestCase(unittest.TestCase):
    """认证测试用例"""
    
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
    
    def test_register(self):
        """测试用户注册"""
        response = self.client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123',
            'agree_terms': True,
            'csrf_token': self._get_csrf_token()
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
    
    def test_login(self):
        """测试用户登录"""
        # 先创建用户
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # 登录
        response = self.client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'password123',
            'csrf_token': self._get_csrf_token()
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
    
    def test_login_failure(self):
        """测试登录失败"""
        response = self.client.post('/auth/login', data={
            'username': 'nonexistent',
            'password': 'wrongpassword',
            'csrf_token': self._get_csrf_token()
        })
        
        self.assertEqual(response.status_code, 200)
    
    def _get_csrf_token(self):
        """获取 CSRF token（简化版）"""
        response = self.client.get('/auth/register')
        # 在实际测试中，需要从响应中提取 CSRF token
        # 这里返回空字符串，实际使用时需要正确提取
        return ''


if __name__ == '__main__':
    unittest.main()

