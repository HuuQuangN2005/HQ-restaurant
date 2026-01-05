from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from products.models import Category, Food, Ingredient
from users.models import Account, Phone, Address, UserType


class MyAdminSite(admin.AdminSite):
    site_header = "H&Q Restaurant Management System"
    site_title = "H&Q Admin"


admin_site = MyAdminSite()


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0
    fields = ["phone", "is_default", "is_verify", "is_active"]


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
    fields = ["address", "city", "is_default", "is_active"]


class AccountAdmin(UserAdmin):
    list_display = [
        "uuid",
        "username",
        "email",
        "role",
        "avatar",
        "is_active",
    ]

    list_filter = ["role", "gender", "is_active", "is_approved", "is_staff"]
    search_fields = ["username", "email", "uuid"]
    readonly_fields = ["uuid", "date_joined", "updated_date"]

    fieldsets = (
        (
            None,
            {"fields": ("username", "password")},
        ),
        (
            "Profile",
            {
                "fields": (
                    ("first_name", "last_name"),
                    "email",
                    "gender",
                    "birth_date",
                    "avatar",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "role",
                    "is_approved",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Etcs", {"fields": ("date_joined", "updated_date")}),
    )

    def save_model(self, request, obj, form, change):

        if obj.role.__eq__(UserType.ADMIN):
            obj.is_staff = True
            obj.is_superuser = False
            obj.is_approved = True

        elif obj.role.__eq__(UserType.COOKER):
            obj.is_staff = True
            obj.is_superuser = False

        else:
            obj.is_staff = False
            obj.is_superuser = False
            obj.is_approved = False

        super().save_model(request, obj, form, change)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["uuid", "name", "created_date", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ["uuid", "name", "created_date", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


class FoodAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
        "category",
        "cook_time",
        "image",
        "is_active",
    ]

    search_fields = ["name", "category__name", "ingredients__name"]

    list_filter = ["category", "ingredients", "is_active"]

    readonly_fields = ["uuid", "image", "created_date", "updated_date"]

    filter_horizontal = ["ingredients"]

    fieldsets = (
        (
            "Food detail",
            {
                "fields": (
                    "uuid",
                    "name",
                    "price",
                    "cook_time",
                    "is_active",
                    "image",
                )
            },
        ),
        (
            "Relates",
            {
                "fields": ("category", "ingredients"),
            },
        ),
        (
            "Etcs",
            {
                "fields": ("created_date", "updated_date"),
            },
        ),
    )


admin_site.register(Category, CategoryAdmin)
admin_site.register(Ingredient, IngredientAdmin)
admin_site.register(Food, FoodAdmin)
admin_site.register(Account, AccountAdmin)
admin_site.register(Phone)
admin_site.register(Address)
