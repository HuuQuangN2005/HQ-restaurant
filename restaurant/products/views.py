from rest_framework import viewsets, permissions, generics
from products.serializers import CategorySerializer, FoodSerializer
from products.models import Category, Food
from restaurant.permissions import IsVerifiedCookerOrAdmin


class CategoryViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.filter(is_active=True)
    serializer_class = FoodSerializer

    def get_permissions(self):

        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsVerifiedCookerOrAdmin()]

        return [permissions.AllowAny()]
