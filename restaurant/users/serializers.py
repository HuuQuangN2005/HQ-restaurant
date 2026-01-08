from rest_framework import serializers
from users.models import Account, Phone, Address, UserType, GenderType


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ["uuid", "phone", "is_default", "is_verify"]
        read_only_fields = ["uuid", "is_verify"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["uuid", "address", "city", "is_default"]
        read_only_fields = ["uuid"]


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    image = serializers.ImageField(allow_null=True, required=False)
    email = serializers.EmailField(required=True)
    phones = PhoneSerializer(many=True, read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)

    gender = serializers.ChoiceField(
        choices=GenderType.choices, allow_null=True, required=False
    )

    class Meta:
        model = Account
        fields = [
            "uuid",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "image",
            "birth_date",
            "role",
            "gender",
            "date_joined",
            "phones",
            "addresses",
        ]
        read_only_fields = ["uuid", "date_joined","role"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["role"] = instance.get_role_display()
        data["gender"] = instance.get_gender_display()
        return data

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)
