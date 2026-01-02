from django.db import models, transaction
from uuid import uuid4
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from cloudinary.models import CloudinaryField


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDBaseModel(BaseModel):
    uuid = models.UUIDField(default=uuid4, unique=True, db_index=True, editable=False)

    class Meta:
        abstract = True


class UserRole(models.IntegerChoices):
    ADMIN = 1
    COOKER = 2
    GUEST = 3
    MEMBER = 4


class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")

        extra_fields.setdefault("is_active", True)

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=150, unique=True)
    avatar = CloudinaryField(null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    profile = models.OneToOneField(
        "Profile", on_delete=models.PROTECT, related_name="account"
    )

    objects = AccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user_accounts"
        verbose_name = "Account"

    def __str__(self):
        return self.username


class Profile(UUIDBaseModel):
    first_name = models.CharField(max_length=100, null=True, editable=True)
    last_name = models.CharField(max_length=100, null=True, editable=True)
    address = models.CharField(max_length=150, null=True,editable=True)
