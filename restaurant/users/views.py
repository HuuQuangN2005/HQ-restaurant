from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from users.models import Account, Phone, Address
from users.serializers import AccountSerializer, PhoneSerializer, AddressSerializer
from users.paginators import AccountInfoPaginator


class AccountViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Account.objects.filter(is_active=True)
    serializer_class = AccountSerializer
    lookup_field = "uuid"

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()

    @action(methods=["get", "patch"], detail=False, url_path="me")
    def me(self, request):
        instance = Account.objects.prefetch_related("phones", "addresses").get(
            uuid=request.user.uuid
        )

        if request.method == "GET":
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MyBaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = AccountInfoPaginator
    lookup_field = "uuid"
    http_method_names = ["post", "patch", "delete"]

    def get_queryset(self):
        return self.queryset.filter(account=self.request.user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(account=self.request.user, is_default=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class PhoneViewSet(MyBaseViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer


class AddressViewSet(MyBaseViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
