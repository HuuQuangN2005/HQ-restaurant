from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action

from products.serializers import (
    CategorySerializer,
    FoodSerializer,
    IngredientSerializer,
)
from actions.serializers import CommentSerializer
from products.models import Category, Food, Ingredient
from restaurant.permissions import IsVerifiedCookerOrAdmin
from products.paginators import (
    CategoryPaginator,
    FoodPaginator,
    IngredientPaginator,
    CommentPaginator,
)


class CategoryViewSet(viewsets.GenericViewSet, generics.ListAPIView):

    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    pagination_class = CategoryPaginator
    permission_classes = [permissions.AllowAny]


class IngredientViewSet(viewsets.ModelViewSet):

    queryset = Ingredient.objects.filter(is_active=True)
    serializer_class = IngredientSerializer
    pagination_class = IngredientPaginator
    lookup_field = "uuid"
    http_method_names = ["get", "post", "patch", "delete"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsVerifiedCookerOrAdmin()]
        return [permissions.AllowAny()]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class FoodViewSet(viewsets.ModelViewSet):

    queryset = Food.objects.filter(is_active=True)
    serializer_class = FoodSerializer
    lookup_field = "uuid"
    pagination_class = FoodPaginator
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        queryset = self.queryset.select_related(
            "category", "created_by"
        ).prefetch_related("ingredients")

        params = self.request.query_params
        search_query = params.get("q")
        chef_uuid = params.get("chef")
        category_uuid = params.get("category")
        min_price = params.get("min_price")
        max_price = params.get("max_price")
        max_time = params.get("max_time")
        ordering = params.get("ordering")

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        if chef_uuid:
            queryset = queryset.filter(created_by__uuid=chef_uuid)
        if category_uuid:
            queryset = queryset.filter(category__uuid=category_uuid)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if max_time:
            queryset = queryset.filter(cook_time__lte=max_time)

        valid_ordering = ["name", "-name", "price", "-price", "cook_time", "-cook_time"]
        if ordering in valid_ordering:
            queryset = queryset.order_by(ordering)

        return queryset

    @action(methods=["get", "post"], url_path="comments", detail=True)
    def handle_comments(self, request, uuid=None):
        food_instance = self.get_object()

        if request.method == "POST":
            serializer = CommentSerializer(
                data={
                    "content": request.data.get("content"),
                    "account": request.user.pk,
                    "food": food_instance.pk,
                }
            )
            serializer.is_valid(raise_exception=True)
            comment = serializer.save()
            return Response(
                CommentSerializer(comment).data, status=status.HTTP_201_CREATED
            )

        comments = food_instance.comment_set.select_related("account").filter(
            is_active=True
        )

        paginator = CommentPaginator()
        page = paginator.paginate_queryset(comments, request)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action.__eq__("handle_comments") and self.request.method.__eq__("POST"):
            return [permissions.IsAuthenticated()]

        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsVerifiedCookerOrAdmin()]

        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
