from rest_framework import serializers
from products.models import Category, Ingredient, Food


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Category
        fields = ["uuid", "name", "image"]
        read_only_fields = ["uuid"]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["uuid", "name"]
        read_only_fields = ["uuid"]


class FoodSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    cooker_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    image = serializers.ImageField(read_only=True)
    
    category_id = serializers.SlugRelatedField(
        queryset=Category.objects.filter(is_active=True),
        slug_field="uuid",
        source="category",
        write_only=True,
    )

    class Meta:
        model = Food
        fields = [
            "uuid", "name", "price", "description", 
            "image", "cook_time", "category", "category_id", 
            "cooker_name", "created_by", "created_date"
        ]
        read_only_fields = ["uuid", "created_by", "created_date"]


class FoodDetailSerializer(FoodSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    ingredient_uuids = serializers.SlugRelatedField(
        many=True,
        queryset=Ingredient.objects.filter(is_active=True),
        slug_field="uuid",
        source="ingredients",
        write_only=True,
        required=False,
    )

    class Meta(FoodSerializer.Meta):
        fields = FoodSerializer.Meta.fields + ["ingredients", "ingredient_uuids"]
