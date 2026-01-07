from rest_framework import viewsets, permissions, generics
from products.serializers import (
    CategorySerializer,
    FoodSerializer,
)
from products.models import Category, Food
from restaurant.permissions import IsVerifiedCookerOrAdmin
from products.paginators import CategoryPaginator, FoodPaginator


class CategoryViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    pagination_class = CategoryPaginator
    permission_classes = [permissions.AllowAny]


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.filter(is_active=True)
    serializer_class = FoodSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        queryset = self.queryset.select_related("category", "created_by")
        params = self.request.query_params

        q = params.get("q")
        chef_uuid = params.get("chef")
        cat_uuid = params.get("category")
        min_p = params.get("min_price")
        max_p = params.get("max_price")
        max_t = params.get("max_time")
        ordering = params.get("ordering")

        if q:
            queryset = queryset.filter(name__icontains=q)
        if chef_uuid:
            queryset = queryset.filter(created_by__uuid=chef_uuid)
        if cat_uuid:
            queryset = queryset.filter(category__uuid=cat_uuid)
        if min_p:
            queryset = queryset.filter(price__gte=min_p)
        if max_p:
            queryset = queryset.filter(price__lte=max_p)
        if max_t:
            queryset = queryset.filter(cook_time__lte=max_t)

        if ordering in [
            "name",
            "-name",
            "price",
            "-price",
            "created_date",
            "-created_date",
        ]:
            queryset = queryset.order_by(ordering)

        return queryset

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsVerifiedCookerOrAdmin()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
