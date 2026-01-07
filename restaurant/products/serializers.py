from rest_framework import serializers
from products.models import Category, Ingredient, Food


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Category
        fields = ["uuid", "name", "image"]
        read_only_fields = ["uuid"]


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["uuid", "name"]
        read_only_fields = ["uuid", "name"]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["uuid", "name"]
        read_only_fields = ["uuid", "name"]


class FoodSerializer(serializers.ModelSerializer):
    category = SimpleCategorySerializer(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)

    chef_name = serializers.CharField(source="created_by.get_full_name", read_only=True)

    category_id = serializers.SlugRelatedField(
        queryset=Category.objects.filter(is_active=True),
        slug_field="uuid",
        source="category",
        write_only=True,
    )

    class Meta:
        model = Food
        fields = [
            "uuid",
            "name",
            "price",
            "description",
            "image",
            "cook_time",
            "category",
            "category_id",
            "chef_name",
            "created_date",
        ]
        read_only_fields = ["uuid", "created_date"]


class SimpleFoodSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Food
        fields = ["uuid", "name", "image", "price"]
        read_only_fields = ["uuid", "image", "name", "price"]


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
