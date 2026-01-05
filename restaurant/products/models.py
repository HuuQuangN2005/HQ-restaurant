from django.db import models
from uuid import uuid4
from ckeditor_uploader.fields import RichTextUploadingField
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator


class UUIDBaseModel(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, db_index=True, editable=False)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(UUIDBaseModel):
    name = models.CharField(max_length=50, unique=True)
    image = CloudinaryField(
        folder="restaurant/foods",
        default="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767486978/default_avatar_vcrsot.jpg",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "products_categories"


class Ingredient(UUIDBaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "products_ingredients"


class Food(UUIDBaseModel):
    name = models.CharField(max_length=255, null=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    cook_time = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    description = RichTextUploadingField(null=True, blank=True)
    image = CloudinaryField(
        folder="restaurant/foods",
        default="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767486978/default_avatar_vcrsot.jpg",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="foods",
    )

    ingredients = models.ManyToManyField("Ingredient", null=True, related_name="foods")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "products_foods"
