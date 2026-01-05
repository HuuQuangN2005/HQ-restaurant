from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import AccountViewSet, CurrentUserViewSet, PhoneViewSet, AddressViewSet

router = DefaultRouter()

router.register(
    r"accounts/current-user/phones", PhoneViewSet, basename="current-user-phones"
)
router.register(
    r"accounts/current-user/addresses",
    AddressViewSet,
    basename="current-user-addresses",
)
router.register(r"accounts", CurrentUserViewSet, basename="current-user")
router.register(r"accounts", AccountViewSet, basename="account")

urlpatterns = [
    
    path("", include(router.urls)),
]
