from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from users.models import Account, Phone, Address
from users.serializers import AccountSerializer, PhoneSerializer, AddressSerializer
from users.paginators import AccountInfoPaginator


class AccountViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Account.objects.filter(is_active=True)
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]


class CurrentUserViewSet(viewsets.GenericViewSet):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    @action(methods=["get"], detail=False, url_path="current-user")
    def get_current_user(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=["patch"], detail=False, url_path="current-user/edit")
    def edit(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MyBaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = AccountInfoPaginator
    lookup_field = "uuid"
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return (
            self.queryset.filter(account=self.get_object(), is_active=True)
            .select_related("account")
            .order_by("-is_default", "-created_date")
        )

    def perform_create(self, serializer):
        serializer.save(account=self.get_object())

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class PhoneViewSet(MyBaseViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer


class AddressViewSet(MyBaseViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
