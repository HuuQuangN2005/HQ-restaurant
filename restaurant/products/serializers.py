from rest_framework import serializers
from products.models import Category, Ingredient, Food


class ImageSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)

        image = getattr(instance, "image", None)
        if image:
            if isinstance(image, str):
                data["image"] = image
            elif hasattr(image, "url"):
                data["image"] = image.url
            else:
                data["image"] = str(image)
        return data


class CategorySerializer(ImageSerializer):
    class Meta:
        model = Category
        fields = ["uuid", "name", "image"]
        extra_kwargs = {
            "uuid": {"read_only": True},
            "image": {"read_only": True},
        }


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["uuid", "name"]


class FoodSerializer(ImageSerializer):
    category = CategorySerializer(read_only=True)

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
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
            "price": {"min_value": 0},
            "cook_time": {"min_value": 0},
        }



class FoodDetailSerializer(FoodSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta(FoodSerializer.Meta):
        fields = FoodSerializer.Meta.fields + ["ingredients"]
