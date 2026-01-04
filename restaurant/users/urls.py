from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import AccountViewSet

router = DefaultRouter()


router.register(r"accounts", AccountViewSet, basename="account")

urlpatterns = [
    path("", include(router.urls)),
]
