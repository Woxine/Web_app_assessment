import os

meal_images = [
    'Beetroot_Soup.png',
    'Cooked_Rice.webp',
    'Fried_Rice.webp',
    'Ham.webp',
    'Mixed_Salad.webp',
    'Smoked_Ham.webp',
    'Stuffed_Pumpkin_Block.webp',
    'Tomato_Sauce.webp'
]

print('检查图片文件存在性:')
base_path = 'app/static/images/meal/'

for img in meal_images:
    exists = os.path.exists(base_path + img)
    status = "存在" if exists else "不存在"
    print(f'✓ {img}: {status}')