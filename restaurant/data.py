import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant.settings")

django.setup()

from products.models import Category, Ingredient, Food

def create_cates():
    file_path = "./data/categories.json" 
    
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        obj, created = Category.objects.update_or_create(
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
        obj, created = Ingredient.objects.update_or_create(
            name=item['name'],
        )



if __name__ == "__main__":
    create_cates()
    create_ingredients()




