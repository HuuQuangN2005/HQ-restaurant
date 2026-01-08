from django.db import models, transaction
from uuid import uuid4
from django.contrib.auth.models import (
    UserManager,
    AbstractUser,
)
from cloudinary.models import CloudinaryField


class UUIDBaseModel(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, db_index=True, editable=False)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserType(models.IntegerChoices):
    ADMIN = 1
    COOKER = 2
    CUSTOMER = 3


class GenderType(models.IntegerChoices):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class AccountManager(UserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        role = extra_fields.get("role")

        if role == UserType.ADMIN:
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", False)
            extra_fields.setdefault("is_approved", True)

        return super().create_user(username, email, password, **extra_fields)

    async def acreate_user(self, username, email=None, password=None, **extra_fields):
        role = extra_fields.get("role")

        if role == UserType.ADMIN:
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", False)
            extra_fields.setdefault("is_approved", True)

        return await super().acreate_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):

        extra_fields.setdefault("role", UserType.ADMIN)
        extra_fields.setdefault("is_approved", True)

        return super().create_superuser(username, email, password, **extra_fields)

    async def acreate_superuser(
        self, username, email=None, password=None, **extra_fields
    ):

        extra_fields.setdefault("role", UserType.ADMIN)
        extra_fields.setdefault("is_approved", True)

        return await super().acreate_superuser(
            username=username, email=email, password=password, **extra_fields
        )


class Account(AbstractUser):
    uuid = models.UUIDField(default=uuid4, unique=True, db_index=True, editable=False)
    image = CloudinaryField(
        null=True,
        folder="restaurant/avatars",
        default="https://res.cloudinary.com/dj7cywkaw/image/upload/v1767486978/default_avatar_vcrsot.jpg",
    )
    email = models.EmailField(unique=True)
    birth_date = models.DateField(null=True,blank=True)
    updated_date = models.DateTimeField(auto_now=True)

    role = models.PositiveSmallIntegerField(
        choices=UserType.choices, default=UserType.CUSTOMER
    )
    gender = models.PositiveSmallIntegerField(
        choices=GenderType.choices, default=GenderType.OTHER
    )

    is_approved = models.BooleanField(default=False)

    objects = AccountManager()

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        db_table = "users_accounts"
        verbose_name = "Account"


class Phone(UUIDBaseModel):
    uuid = models.UUIDField(default=uuid4, unique=True, db_index=True, editable=False)
    phone = models.CharField(max_length=15, unique=True)
    is_default = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)

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

    class Meta:
        db_table = "users_phones"


class Address(UUIDBaseModel):
    uuid = models.UUIDField(default=uuid4, unique=True, db_index=True, editable=False)
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

    class Meta:
        db_table = "users_addresses"
