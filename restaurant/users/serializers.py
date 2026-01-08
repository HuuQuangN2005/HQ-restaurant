from rest_framework import serializers
from users.models import Account, Phone, Address


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ["uuid", "phone", "is_default"]
        read_only_fields = ["uuid"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["uuid", "address", "city", "is_default"]
        read_only_fields = ["uuid"]


class SimpleAccountSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = Account
        fields = ["uuid", "username", "image"]


class AccountSerializer(SimpleAccountSerializer):
    password = serializers.CharField(write_only=True)
    phones = PhoneSerializer(many=True, read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = SimpleAccountSerializer.Meta.model
        fields = SimpleAccountSerializer.Meta.fields + [
            "password",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "role",
            "gender",
            "date_joined",
            "phones",
            "addresses",
            "is_approved",
        ]

        read_only_fields = ["uuid", "date_joined", "is_approved", "role"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["role"] = instance.get_role_display()
        data["gender"] = instance.get_gender_display()

        return data

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)
