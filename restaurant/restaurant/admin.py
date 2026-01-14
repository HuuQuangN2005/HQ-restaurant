from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.db.models import Sum, F
from django.urls import path
from django.template.response import TemplateResponse
from django.apps import apps
from django.db.models.functions import TruncMonth, TruncDay, TruncYear

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from unfold.admin import ModelAdmin, TabularInline, display as unfold_display
from unfold.sites import UnfoldAdminSite
from users.models import UserType

import json

# --- 1. CUSTOM ADMIN SITE ---
class MyAdminSite(UnfoldAdminSite):
    site_header = "H&Q Restaurant Management System"
    site_title = "H&Q Admin"

    def get_urls(self):
        return [path("stats/", self.admin_view(self.stats_view))] + super().get_urls()

    def stats_view(self, request):
        OrderModel = apps.get_model("actions", "Order")
        OrderDetailModel = apps.get_model("actions", "OrderDetail")
        ReservationModel = apps.get_model("actions", "Reservation")

        # --- LẤY THAM SỐ FILTER ---
        period = request.GET.get("period", "month")  # mặc định theo tháng

        if period == "day":
            trunc_func = TruncDay("order__created_date")
            line_trunc = TruncDay("created_date")
        elif period == "year":
            trunc_func = TruncYear("order__created_date")
            line_trunc = TruncYear("created_date")
        else:
            trunc_func = TruncMonth("order__created_date")
            line_trunc = TruncMonth("created_date")

        # --- DATA CHO ĐẦU BẾP (List & Bar Chart) ---
        # 1. Danh sách món ăn (không giới hạn để Search được tất cả)
        all_food_stats = (
            OrderDetailModel.objects.filter(order__is_paid=True)
            .values("food__name")
            .annotate(
                total_qty=Sum("quantity"),
                total_rev=Sum(F("quantity") * F("price")),
            )
            .order_by("-total_rev")
        )

        # 2. Top 5 món ăn theo filter thời gian (cho Bar Chart)
        bar_chart_data = (
            OrderDetailModel.objects.filter(order__is_paid=True)
            .values("food__name")
            .annotate(
                total_rev=Sum(F("quantity") * F("price")),
            )
            .order_by("-total_rev")[:5]
        )

        # --- DATA CHO ADMIN (Line Chart) ---
        line_chart_data = (
            OrderModel.objects.filter(is_paid=True)
            .annotate(time_label=line_trunc)
            .values("time_label")
            .annotate(total=Sum("total_price"))
            .order_by("time_label")
        )

        # Định dạng dữ liệu cho Chart.js
        line_labels = [
            (
                item["time_label"].strftime("%d/%m/%Y")
                if period == "day"
                else (
                    item["time_label"].strftime("%m/%Y")
                    if period == "month"
                    else item["time_label"].strftime("%Y")
                )
            )
            for item in line_chart_data
        ]
        line_values = [float(item["total"]) for item in line_chart_data]

        bar_labels = [item["food__name"] for item in bar_chart_data]
        bar_values = [float(item["total_rev"]) for item in bar_chart_data]

        context = {
            **self.each_context(request),
            "title": "Báo cáo nhà hàng",
            "all_food_stats": all_food_stats[:10],  # Chỉ hiện 10 món ban đầu
            "full_food_data_json": json.dumps(
                list(all_food_stats), default=str
            ),  # Dùng cho search JS
            "bar_labels": json.dumps(bar_labels),
            "bar_values": json.dumps(bar_values),
            "line_labels": json.dumps(line_labels),
            "line_values": json.dumps(line_values),
            "total_res": ReservationModel.objects.count(),
            "period": period,
            "is_admin": request.user.is_superuser,
        }
        return TemplateResponse(request, "admin/stats.html", context)


admin_site = MyAdminSite()


class FoodForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["description"].widget = CKEditorUploadingWidget()


class PhoneInline(TabularInline):
    model = apps.get_model("users", "Phone")
    extra = 0


class AddressInline(TabularInline):
    model = apps.get_model("users", "Address")
    extra = 0


class OrderDetailInline(TabularInline):
    model = apps.get_model("actions", "OrderDetail")
    fields = ["food", "quantity", "price", "get_total"]
    readonly_fields = ["get_total", "price"]
    extra = 1

    @unfold_display(description="Total")
    def get_total(self, obj):
        if obj.quantity and obj.price:
            total_amount = obj.quantity * obj.price
            return f"{total_amount:,.0f} VNĐ"
        return "0 VNĐ"


@admin.register(apps.get_model("users", "Account"), site=admin_site)
class AccountAdmin(UserAdmin, ModelAdmin):
    inlines = [PhoneInline, AddressInline]
    list_display = [
        "uuid",
        "username",
        "email",
        "display_role",
        "is_approved",
        "is_active",
    ]
    list_filter = ["role", "gender", "is_active", "is_approved", "is_staff"]
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

    @unfold_display(description="Role")
    def display_role(self, obj):
        return obj.get_role_display()

    def save_model(self, request, obj, form, change):
        if obj.role == UserType.ADMIN:
            obj.is_staff, obj.is_superuser, obj.is_approved = True, True, True
        elif obj.role == UserType.COOKER:
            obj.is_staff, obj.is_superuser = True, False
        elif obj.role == UserType.CUSTOMER:
            obj.is_staff, obj.is_superuser, obj.is_approved = False, False, False

        super().save_model(request, obj, form, change)


@admin.register(apps.get_model("actions", "Order"), site=admin_site)
class OrderAdmin(ModelAdmin):
    list_display = [
        "uuid",
        "account",
        "total_price_formatted",
        "status",
        "is_paid",
        "created_date",
        "is_active",
    ]
    inlines = [OrderDetailInline]
    readonly_fields = ["uuid", "total_price", "created_date", "updated_date"]
    list_filter = ["status", "is_paid", "is_active"]

    @unfold_display(description="Order Total")
    def total_price_formatted(self, obj):
        return f"{obj.total_price:,.0f} VNĐ"


@admin.register(apps.get_model("actions", "Reservation"), site=admin_site)
class ReservationAdmin(ModelAdmin):
    list_display = ["uuid", "account", "status", "created_date", "is_active"]
    readonly_fields = ["uuid", "created_date", "updated_date"]
    list_filter = ["status", "is_active"]


@admin.register(apps.get_model("actions", "Comment"), site=admin_site)
class CommentAdmin(ModelAdmin):
    list_display = ["uuid", "account", "food", "created_date", "is_active"]
    readonly_fields = ["uuid", "created_date", "updated_date"]
    list_filter = ["is_active"]


class MyCustomAdmin(ModelAdmin):
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return request.user.is_staff and request.user.is_approved

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_add_permission(self, request):
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_delete_permission(self, request, obj=None):
        return self.has_module_permission(request)


@admin.register(apps.get_model("products", "Food"), site=admin_site)
class FoodAdmin(MyCustomAdmin):
    form = FoodForm
    list_display = ["uuid", "name", "price_formatted", "category", "is_active"]
    readonly_fields = ["uuid", "created_by", "created_date", "updated_date"]
    filter_horizontal = ["ingredients"]
    list_filter = ["category", "is_active"]

    @unfold_display(description="Price")
    def price_formatted(self, obj):
        return f"{obj.price:,.0f} VNĐ"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(apps.get_model("products", "Category"), site=admin_site)
class CategoryAdmin(MyCustomAdmin):
    list_display = ["uuid", "name", "is_active"]
    readonly_fields = ["uuid", "created_date", "updated_date"]
    search_fields = ["name"]


@admin.register(apps.get_model("products", "Ingredient"), site=admin_site)
class IngredientAdmin(MyCustomAdmin):
    list_display = ["uuid", "name", "is_active"]
    readonly_fields = ["uuid", "created_date", "updated_date"]
    search_fields = ["name"]
