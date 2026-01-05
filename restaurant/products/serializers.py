from rest_framework import serializers
from products.models import Category, Ingredient, Food
import logging

logger = logging.getLogger(__name__)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["uuid", "name"]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["uuid", "name"]


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = [
            "uuid",
            "name",
            "price",
            "description",
            "image",
            "cook_time",
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

        except Exception as e:
            logger.error(f"Foods serializer: {str(e)}")

        return data
