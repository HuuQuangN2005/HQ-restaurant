import os
import django
import json
import random
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant.settings")

django.setup()

from products.models import Category, Ingredient, Food
from users.models import Account, UserType

def create_cates():
    file_path = "./data/categories.json" 
    
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        cate, created = Category.objects.update_or_create(
            name=item['name'],
            defaults={'image': item['image']}
        )

def create_ingredients():
    file_path = "./data/ingredients.json" 
    
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        ingredient, created = Ingredient.objects.update_or_create(
            name=item['name'],
        )



def create_foods():
    file_path = "./data/foods.json" 
    
    if not os.path.exists(file_path):
        return
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    creator = Account.objects.filter(is_superuser=True).first()
    if not creator:
        return

    for item in data:
        cate, _ = Category.objects.get_or_create(
            name=item['category']
        )

        food, _ = Food.objects.update_or_create(
            name=item['name'],
            defaults={
                'description': item.get('description', ''),
                'price': item.get('price', (random.randrange(50, 201, 10) - 1) * 1000 ), 
                'cook_time': item.get('cook_time', random.randrange(10, 31, 5)),
                'image': item.get('image', ''),
                'category': cate,
                'created_by': creator,
            }
        )

        if 'ingredients' in item:
            
            ingredients = []
            for ingredient_name in item['ingredients']:
                ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
                ingredients.append(ingredient)
                
            food.ingredients.set(ingredients)
            

    
if __name__ == "__main__":
    create_cates()
    create_foods()
    create_ingredients()




