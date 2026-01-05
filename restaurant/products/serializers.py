from rest_framework import serializers
from products.models import Category, Tag, Ingredient, Food
import logging

logger = logging.getLogger(__name__)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["uuid", "name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["uuid", "name"]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["uuid", "name"]


class FoodSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        source="tags",
        write_only=True,
        required=False,
    )
    ingredient_ids = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        many=True,
        source="ingredients",
        write_only=True,
        required=False,
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
            "tags",
            "tag_ids",
            "ingredients",
            "ingredient_ids",
            "created_date",
            "updated_date",
        ]

    def to_representation(self, instance):
        try:
            data = super().to_representation(instance)

            if instance.avatar:
                if isinstance(instance.avatar, str):
                    data["avatar"] = instance.avatar
                elif hasattr(instance.avatar, "url"):
                    data["avatar"] = instance.avatar.url
                else:
                    data["avatar"] = str(instance.avatar)

            data["role"] = instance.get_role_display()
            data["gender"] = instance.get_gender_display()

        except Exception as e:
            logger.error(f"Users serializer: {str(e)}")

        return data
