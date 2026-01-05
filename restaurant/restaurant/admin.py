from django.contrib import admin
from django.utils.safestring import mark_safe
from products.models import Category, Food, Ingredient


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["uuid", "name", "created_date", "is_active"]
    list_filter = ["is_active", "created_date"]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ["uuid", "name", "created_date", "is_active"]
    list_filter = ["is_active", "created_date"]


class FoodAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "name",
        "price",
        "category",
        "cook_time",
        "is_active",
        "image_view",
    ]
    search_fields = ["name", "category__name", "ingredients__name"]
    list_filter = ["category", "ingredients", "is_active"]
    readonly_fields = ["image_view"]

    filter_horizontal = ["ingredients"]

    def image_view(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return "No Image"


class MyAdminSite(admin.AdminSite):
    site_header = "H&Q Restaurant App"


admin_site = MyAdminSite()

admin_site.register(Category, CategoryAdmin)
admin_site.register(Ingredient, IngredientAdmin)
admin_site.register(Food, FoodAdmin)
