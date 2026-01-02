from rest_framework import serializers
from users.models import Account, Employee, Customer
from django.db import transaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["username", "password", "avatar"]
        extra_kwargs = {
            "password": {"write_only": True},
            "avatar": {"required": False},
            "username": {"validators": []},
        }

    def validate_username(self, value):
        if Account.objects.filter(username=value).exists():
            raise serializers.ValidationError("Tên tài khoản này đã được sử dụng.")
        return value

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["avatar"] = instance.avatar.url if instance.avatar else ""

        return data


class EmployeeSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = Employee
        fields = [
            "uuid",
            "first_name",
            "last_name",
            "role",
            "gmail",
            "phone",
            "account",
        ]

    def create(self, validated_data):
        account_data = validated_data.pop("account")
        username = account_data.get("username")

        with transaction.atomic():
            account = Account.objects.filter(username=username, is_active=True).first()

            if account:
                if hasattr(account, "employees") or hasattr(account, "customers"):
                    raise serializers.ValidationError(
                        {"Error": "This account is already linked to another profile."}
                    )

                password = account_data.get("password")
                if password:
                    account.set_password(password)
                    account.save()
            else:
                try:
                    account = Account.objects.create_user(**account_data)
                except Exception:
                    raise serializers.ValidationError(
                        {"Error": "Username already exists or is invalid."}
                    )

            employee = Employee.objects.create(account=account, **validated_data)

        return employee


class CustomerSerializer(serializers.ModelSerializer):
    account = AccountSerializer(required=False, allow_null=True)

    class Meta:
        model = Customer
        fields = [
            "uuid",
            "first_name",
            "last_name",
            "address",
            "birth_date",
            "gender",
            "gmail",
            "phone",
            "role",
            "account",
        ]

    def create(self, validated_data):
        account_data = validated_data.pop("account", None)

        with transaction.atomic():
            account = None
            if account_data:
                account = Account.objects.create_user(**account_data)

            customer = Customer.objects.create(account=account, **validated_data)

        return customer
