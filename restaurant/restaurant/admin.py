from django.contrib import admin
from django.utils.safestring import mark_safe
from products.models import Category, Tag, Food, Ingredient


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["uuid", "name", "created_date", "is_active"]
    list_filter = ["is_active", "created_date"]


class FoodAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "category", "cook_time", "is_active", "image_view"]
    search_fields = ["name", "category__name", "tag__name"]
    list_filter = ["category", "tags", "is_active"]
    readonly_fields = ["image_view"]

    def image_view(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="240" />')
        return "No Image"

    image_view.short_description = "Preview"


class MyAdminSite(admin.AdminSite):
    site_header = "H&Q Restaurant App"


admin_site = MyAdminSite()

admin_site.register(Category, CategoryAdmin)
admin_site.register(Tag)
admin_site.register(Ingredient)
admin_site.register(Food, FoodAdmin)
