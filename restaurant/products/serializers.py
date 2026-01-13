from rest_framework import serializers
from products.models import Category, Ingredient, Food
from django.db import transaction


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["uuid", "name"]
        read_only_fields = ["uuid"]


class CategorySerializer(SimpleCategorySerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = SimpleCategorySerializer.Meta.model
        fields = SimpleCategorySerializer.Meta.fields + ["image"]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["uuid", "name"]
        read_only_fields = ["uuid"]


class SimpleFoodSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Food
        fields = ["uuid", "name", "image", "price", "cook_time"]
        read_only_fields = ["uuid"]


class FoodSerializer(SimpleFoodSerializer):
    category_uuid = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="uuid",
        source="category",
        write_only=True,
    )

    ingredients = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = SimpleFoodSerializer.Meta.model
        fields = SimpleFoodSerializer.Meta.fields + [
            "category",
            "category_uuid",
            "created_by",
            "description",
            "ingredients",
        ]
        read_only_fields = ["uuid", "created_date", "created_by", "category"]

    def _process_ingredients(self, ingredients):
        objs = []

        if ingredients:
            for ingredient in ingredients:
                ingredient = ingredient.strip()

                if ingredient:
                    obj, _ = Ingredient.objects.get_or_create(name=ingredient)
                    objs.append(obj)

        return objs

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients", [])

        with transaction.atomic():
            food = Food.objects.create(**validated_data)

            if ingredients:
                objs = self._process_ingredients(ingredients)
                food.ingredients.set(objs)

        return food

    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients", None)

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            if ingredients is not None:
                objs = self._process_ingredients(ingredients)
                instance.ingredients.set(objs)

        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.category:
            data["category"] = instance.category.name

        if instance.created_by:
            data["created_by"] = instance.created_by.get_full_name()

        if instance.ingredients:
            data["ingredients"] = list(
                instance.ingredients.values_list("name", flat=True)
            )
        return data
