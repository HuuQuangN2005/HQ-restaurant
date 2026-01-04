from rest_framework import viewsets, permissions, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers import AccountSerializer, PhoneSerializer, AddressSerializer
from users.models import Account, Phone, Address


class AccountViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Account.objects.filter(is_active=True)
    serializer_class = AccountSerializer
    lookup_field = "uuid"

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

    # --- Profile ---
    @action(methods=["get", "patch"], detail=False, url_path="current-user")
    def current_user(self, request):
        user = request.user
        if request.method == "PATCH":
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(self.get_serializer(user).data)

    # --- Phones ---
    @action(methods=["get", "post"], detail=False, url_path="current-user/phones")
    def current_user_phones(self, request):
        if request.method == "GET":
            phones = Phone.objects.filter(account=request.user, is_active=True)
            return Response(PhoneSerializer(phones, many=True).data)

        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(account=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=["patch", "delete"],
        detail=False,
        url_path=r"current-user/phones/(?P<uuid>[^/.]+)",
    )
    def manage_phone(self, request, uuid=None):
        phone = Phone.objects.filter(
            account=request.user, uuid=uuid, is_active=True
        ).first()
        if not phone:
            return Response(
                {"detail": "Phone not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if request.method == "PATCH":
            serializer = PhoneSerializer(phone, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        phone.is_active = False
        phone.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # --- Addresses ---
    @action(methods=["get", "post"], detail=False, url_path="current-user/addresses")
    def current_user_addresses(self, request):
        if request.method == "GET":
            addresses = Address.objects.filter(account=request.user, is_active=True)
            return Response(AddressSerializer(addresses, many=True).data)

        serializer = AddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(account=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=["patch", "delete"],
        detail=False,
        url_path=r"current-user/addresses/(?P<uuid>[^/.]+)",
    )
    def manage_address(self, request, uuid=None):
        address = Address.objects.filter(
            account=request.user, uuid=uuid, is_active=True
        ).first()
        if not address:
            return Response(
                {"detail": "Address not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if request.method == "PATCH":
            serializer = AddressSerializer(address, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        address.is_active = False
        address.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
