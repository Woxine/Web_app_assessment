"""
Flask-WTF Form Definitions
"""
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, TextAreaField,
    SelectField, RadioField, BooleanField, IntegerField, FloatField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
)
from app.models import User


class RegistrationForm(FlaskForm):
    """Registration Form"""
    # 1. Text Input Field
    username = StringField('Username', validators=[
        DataRequired(message='Please enter username'),
        Length(min=3, max=20, message='Username must be between 3-20 characters')
    ])

    # 1. Text Input Field
    email = StringField('Email', validators=[
        DataRequired(message='Please enter email'),
        Email(message='Please enter a valid email address')
    ])

    # 2. Password Input Field
    password = PasswordField('Password', validators=[
        DataRequired(message='Please enter password'),
        Length(min=8, message='Password must be at least 8 characters')
    ])

    # 2. Password Input Field
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm password'),
        EqualTo('password', message='Passwords do not match')
    ])

    # 6. Checkbox
    agree_terms = BooleanField('I agree to the terms of service', validators=[
        DataRequired(message='Please agree to the terms of service')
    ])

    # 3. Submit Button
    submit = SubmitField('Register')

    def validate_username(self, username):
        """Validate username uniqueness"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'This username is already taken, please choose another.')

    def validate_email(self, email):
        """Validate email uniqueness"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'This email is already registered, please use another.')

    def validate_password(self, password):
        """Validate password strength"""
        pwd = password.data
        if len(pwd) < 8:
            raise ValidationError('Password must be at least 8 characters.')
        if not any(c.isalpha() for c in pwd):
            raise ValidationError('Password must contain at least one letter.')
        if not any(c.isdigit() for c in pwd):
            raise ValidationError('Password must contain at least one number.')


class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField('Username or Email', validators=[
        DataRequired(message='Please enter username or email')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Please enter password')
    ])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    """Search Form (with multiple controls)"""
    # 1. Text Input Field
    keyword = StringField('Search Keyword', validators=[
        DataRequired(message='Please enter search keyword')
    ])

    # 5. Radio Buttons
    search_type = RadioField(
        'Search Type',
        choices=[('all', 'All'), ('crops', 'Crops'), ('meals', 'Meals')],
        default='all',
        validators=[DataRequired()]
    )

    # 4. Dropdown List (Multiple Options)
    sort_by = SelectField(
        'Sort By',
        choices=[
            ('name', 'By Name (A-Z)'),
            ('hunger', 'By Hunger Restored (Desc)'),
            ('likes', 'By Likes (Desc)')
        ],
        default='name',
        validators=[DataRequired()]
    )

    # 3. Submit Button
    submit = SubmitField('Search')


class ProfileEditForm(FlaskForm):
    """User Profile Edit Form"""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=20)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    submit = SubmitField('Save Changes')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already taken.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already registered.')


class CropForm(FlaskForm):
    """Crop Form (for Flask-Admin or manual addition)"""
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    image_url = StringField('Image URL')
    hunger_points = IntegerField('Hunger Restored', validators=[NumberRange(min=0)])
    submit = SubmitField('Submit')


class MealForm(FlaskForm):
    """Meal Form (for Flask-Admin or manual addition)"""
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    image_url = StringField('Image URL')
    hunger_restored = IntegerField('Hunger Restored', validators=[NumberRange(min=0)])
    saturation = FloatField('Saturation', validators=[NumberRange(min=0.0)])
    submit = SubmitField('Submit')
