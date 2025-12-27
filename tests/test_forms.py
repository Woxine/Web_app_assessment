"""
表单验证测试
"""
import unittest
from app import create_app
from app.forms import RegistrationForm, LoginForm, SearchForm


class FormTestCase(unittest.TestCase):
    """表单测试用例"""
    
    def setUp(self):
        """测试前准备"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
    
    def tearDown(self):
        """测试后清理"""
        self.app_context.pop()
    
    def test_registration_form_validation(self):
        """测试注册表单验证"""
        form = RegistrationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123',
            'agree_terms': True
        })
        
        self.assertTrue(form.validate())
    
    def test_registration_form_weak_password(self):
        """测试弱密码验证"""
        form = RegistrationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': '12345678',  # 只有数字，没有字母
            'password2': '12345678',
            'agree_terms': True
        })
        
        self.assertFalse(form.validate())
        self.assertIn('密码必须包含至少一个字母', str(form.password.errors))
    
    def test_registration_form_short_password(self):
        """测试短密码验证"""
        form = RegistrationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'short',
            'password2': 'short',
            'agree_terms': True
        })
        
        self.assertFalse(form.validate())
    
    def test_registration_form_password_mismatch(self):
        """测试密码不匹配"""
        form = RegistrationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password456',
            'agree_terms': True
        })
        
        self.assertFalse(form.validate())
        self.assertIn('两次输入的密码不一致', str(form.password2.errors))
    
    def test_search_form_validation(self):
        """测试搜索表单验证"""
        form = SearchForm(data={
            'keyword': '测试',
            'search_type': 'all',
            'sort_by': 'name'
        })
        
        self.assertTrue(form.validate())


if __name__ == '__main__':
    unittest.main()

