from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import CategoryViewSet, FoodViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("foods", FoodViewSet, basename="food")

urlpatterns = [
    path("", include(router.urls)),
]
