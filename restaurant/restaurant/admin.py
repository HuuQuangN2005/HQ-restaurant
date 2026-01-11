from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from products.models import Category, Food, Ingredient
from actions.models import Reservation, Order, OrderDetail, Comment
from users.models import Account, Phone, Address, UserType
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.db.models import Sum, F
from django.urls import path
from django.template.response import TemplateResponse


class MyAdminSite(admin.AdminSite):
    site_header = "H&Q Restaurant Management System"
    site_title = "H&Q Admin"

    def get_urls(self):
        return [path("stats/", self.admin_view(self.stats_view))] + super().get_urls()

    def stats_view(self, request):
        food_stats = (
            OrderDetail.objects.filter(order__is_paid=True)
            .values("food__name")
            .annotate(
                total_quantity=Sum("quantity"),
                total_revenue=Sum(F("quantity") * F("price")),
            )
            .order_by("-total_revenue")
        )

        total_revenue = (
            Order.objects.filter(is_paid=True).aggregate(Sum("total_price"))[
                "total_price__sum"
            ]
            or 0
        )
        total_res = Reservation.objects.count()

        context = {
            **self.each_context(request),
            "food_stats": food_stats,
            "total_revenue": total_revenue,
            "total_res": total_res,
        }
        return TemplateResponse(request, "admin/stats.html", context)


admin_site = MyAdminSite()


class FoodForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), required=False)

    class Meta:
        model = Food
        fields = "__all__"


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
                "fields": (
                    "created_date",
                    "updated_date",
                    "is_active",
                ),
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


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    fields = ["food", "quantity", "price", "get_total"]
    readonly_fields = ["get_total", "price"]
    extra = 1

    def get_total(self, obj):
        if obj.quantity is not None and obj.price is not None:
            return f"{obj.quantity * obj.price:,.0f} VNĐ"
        return "0 VNĐ"


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "account",
        "total_price_formatted",
        "status",
        "is_paid",
        "created_date",
    ]
    list_filter = ["status", "is_paid", "created_date"]
    search_fields = ["account__username", "uuid"]
    inlines = [OrderDetailInline]
    readonly_fields = ["total_price", "created_date"]

    def total_price_formatted(self, obj):
        return f"{obj.total_price:,.0f} VNĐ"

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for obj in formset.deleted_objects:
            obj.delete()

        for instance in instances:
            if not instance.price:
                instance.price = instance.food.price
            instance.save()

        formset.save_m2m()

        total_order_price = sum(
            item.price * item.quantity for item in form.instance.details.all()
        )
        form.instance.total_price = total_order_price
        form.instance.save()

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data["cl"].queryset
            extra_context = extra_context or {}
            extra_context["revenue_summary"] = (
                qs.filter(is_paid=True).aggregate(Sum("total_price"))[
                    "total_price__sum"
                ]
                or 0
            )
        except (AttributeError, KeyError):
            pass
        return response


class ReservationAdmin(admin.ModelAdmin):
    list_display = ["account", "date", "participants", "status"]
    list_filter = ["status", "date"]
    date_hierarchy = "date"


class CommentAdmin(admin.ModelAdmin):
    list_display = ["account", "food", "content", "created_date"]


admin_site.register(Order, OrderAdmin)
admin_site.register(Reservation, ReservationAdmin)
admin_site.register(Comment, CommentAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Ingredient, IngredientAdmin)
admin_site.register(Food, FoodAdmin)
admin_site.register(Account, AccountAdmin)
