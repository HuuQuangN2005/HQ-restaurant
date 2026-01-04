from rest_framework import serializers
from users.models import Account, Phone, Address


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ["uuid", "phone", "is_default", "is_verify"]
        read_only_fields = ["uuid","is_verify"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["uuid", "address", "city", "is_default"]
        read_only_fields = ["uuid"]


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = [
            "uuid",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "avatar",
            "birth_date",
            "role",
            "gender",
            "date_joined",
        ]
        extra_kwargs = {
            "uuid": {"read_only": True},
            "date_joined": {"read_only": True},
            "role": {"read_only": True},
        }

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)

        avatar = getattr(instance, "avatar", None)
        if avatar:
            if isinstance(avatar, str):
                data["avatar"] = avatar
            elif hasattr(avatar, "url"):
                data["avatar"] = avatar.url
            else:
                data["avatar"] = str(avatar)

        data["role"] = instance.get_role_display()
        data["gender"] = instance.get_gender_display()

        return data
