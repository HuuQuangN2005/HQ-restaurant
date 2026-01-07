from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import CategoryViewSet, FoodViewSet, IngredientViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("foods", FoodViewSet, basename="food")
router.register("ingredients",IngredientViewSet, basename = "ingredient" )

urlpatterns = [
    path("", include(router.urls)),
]
