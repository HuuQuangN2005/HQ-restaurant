from django.db import models
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator
from users.models import Account
from restaurant.models import UUIDBaseModel


class Category(UUIDBaseModel):
    name = models.CharField(max_length=50, unique=True)
    image = CloudinaryField(
        folder="restaurant/categories",
        default="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767674690/restaurant/categories/pipzrn8vsyhkk2l5udjy.jpg",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "products_categories"
        ordering = ["id"]


class Ingredient(UUIDBaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "products_ingredients"


class Food(UUIDBaseModel):
    name = models.CharField(max_length=255, null=False)
    price = models.DecimalField(
        max_digits=15, decimal_places=2, validators=[MinValueValidator(0)]
    )
    cook_time = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    description = RichTextField(null=True, blank=True)
    image = CloudinaryField(
        folder="restaurant/foods",
        default="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767628974/loading_screen_osvl00.jpg",
    )

    created_by = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="created_foods"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="foods",
    )

    ingredients = models.ManyToManyField(Ingredient, blank=True, related_name="foods")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "products_foods"
