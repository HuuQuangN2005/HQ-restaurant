from django.db import models, transaction
from uuid import uuid4
from django.contrib.auth.models import (
    UserManager,
    AbstractUser,
)
from cloudinary.models import CloudinaryField
from restaurant.models import UUIDBaseModel


class UserType(models.IntegerChoices):
    ADMIN = 1
    COOKER = 2
    CUSTOMER = 3


class GenderType(models.IntegerChoices):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class AccountManager(UserManager):
    def _set_rules(self, extra_fields):
        role = extra_fields.get("role", UserType.CUSTOMER)

        extra_fields.setdefault("is_approved", False)

        if role == UserType.ADMIN:
            extra_fields["is_staff"] = True
            extra_fields["is_superuser"] = True
            extra_fields["is_approved"] = True
        elif role == UserType.COOKER:
            extra_fields["is_staff"] = True
            extra_fields["is_approved"] = False
        else:
            extra_fields["is_staff"] = False
            extra_fields["is_approved"] = False

        return extra_fields

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields = self._set_rules(extra_fields)
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required!!!!")

        extra_fields.setdefault("role", UserType.ADMIN)
        extra_fields.setdefault("is_approved", True)
        return super().create_superuser(username, email, password, **extra_fields)


class Account(AbstractUser):
    uuid = models.UUIDField(default=uuid4, unique=True, db_index=True, editable=False)
    image = CloudinaryField(
        null=True,
        folder="restaurant/avatars",
        default="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767486978/default_avatar_vcrsot.jpg",
    )
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)

    role = models.PositiveSmallIntegerField(
        choices=UserType.choices, default=UserType.CUSTOMER
    )
    gender = models.PositiveSmallIntegerField(
        choices=GenderType.choices, default=GenderType.OTHER
    )

    is_approved = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["email"]

    objects = AccountManager()

    def __str__(self):
        return self.uuid.__str__()

    class Meta:
        db_table = "users_accounts"
        verbose_name = "Account"


class Phone(UUIDBaseModel):
    phone = models.CharField(max_length=15, unique=True)
    is_default = models.BooleanField(default=False)

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="phones"
    )

    def save(self, *args, **kwargs):
        if self.is_default:
            with transaction.atomic():
                Phone.objects.filter(
                    account=self.account, is_default=True, is_active=True
                ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.uuid.__str__()

    class Meta:
        db_table = "users_phones"


class Address(UUIDBaseModel):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, null=True, blank=True)
    is_default = models.BooleanField(default=False)

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="addresses"
    )

    def save(self, *args, **kwargs):
        if self.is_default:
            with transaction.atomic():
                Address.objects.filter(
                    account=self.account, is_default=True, is_active=True
                ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.uuid.__str__()

    class Meta:
        db_table = "users_addresses"
