from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from products.models import Category, Food, Ingredient
from users.models import Account, Phone, Address, UserType
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MyAdminSite(admin.AdminSite):
    site_header = "H&Q Restaurant Management System"
    site_title = "H&Q Admin"

admin_site = MyAdminSite()

class FoodForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), required=False)

    class Meta:
        model = Food
        fields = '__all__'

class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0

class AddressInline(admin.TabularInline):
    model = Address
    extra = 0


class AccountAdmin(UserAdmin):
    inlines = [PhoneInline, AddressInline]
    list_display = ["uuid", "username", "email", "role", "is_active"]
    list_filter = ["role", "gender", "is_active", "is_approved", "is_staff"]
    search_fields = ["username", "email", "uuid"]
    readonly_fields = ["uuid", "date_joined", "updated_date", "last_login"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Profile",
            {
                "fields": (
                    ("first_name", "last_name"),
                    "gender",
                    "email",
                    "birth_date",
                    "image",
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
        if obj.role == UserType.ADMIN:
            obj.is_staff = True
            obj.is_superuser = True
            obj.is_approved = True
        elif obj.role == UserType.COOKER:
            obj.is_staff = True 
            obj.is_superuser = False
        elif obj.role == UserType.CUSTOMER:
            obj.is_staff = False
            obj.is_superuser = False
            obj.is_approved = False
            
        
        return super().save_model(request, obj, form, change)

class FoodAdmin(admin.ModelAdmin):
    form = FoodForm
    list_display = [
        "uuid",
        "name",
        "price",
        "category",
        "created_by",
        "cook_time",
        "is_active",
    ]

    search_fields = [
        "name",
        "category__name",
        "ingredients__name",
        "created_by__username",
    ]

    list_filter = ["category", "is_active", "created_date"]

    readonly_fields = ["uuid", "created_by", "created_date", "updated_date"]

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
                    "description",
                    "image",
                    "created_by",
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
                "fields": ("created_date", "updated_date", "is_active",),
            },
        ),
    )

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category", "created_by")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["uuid", "name", "created_date", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ["uuid", "name", "created_date", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


admin_site.register(Category, CategoryAdmin)
admin_site.register(Ingredient, IngredientAdmin)
admin_site.register(Food, FoodAdmin)
admin_site.register(Account, AccountAdmin)