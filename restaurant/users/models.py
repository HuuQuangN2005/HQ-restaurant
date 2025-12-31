from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from users.enums import GenderType, CustomerType, EmployeeType
from django.core.exceptions import ValidationError
from django.db import transaction
from uuid import uuid4
from cloudinary.models import CloudinaryField


# -----------------BASE MODEL----------------


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# -----------------ACCOUNT----------------


class AccountManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")

        with transaction.atomic():
            account = self.model(username=username, **extra_fields)
            account.set_password(password)
            account.save(using=self._db)

        return account

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin, BaseModel):

    username = models.CharField(max_length=150, unique=True)
    avatar = CloudinaryField("avatar", null=True, blank=True)

    is_staff = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users_accounts"
        verbose_name = "Account"


# -----------------PROFILE----------------


class Profile(BaseModel):

    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    gender = models.PositiveSmallIntegerField(
        choices=GenderType.choices, default=GenderType.OTHER
    )

    class Meta:
        db_table = "users_profiles"


class Email(BaseModel):

    email = models.EmailField(unique=True)
    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="emails"
    )

    class Meta:
        db_table = "users_emails"


class Phone(BaseModel):

    phone = models.CharField(max_length=20, null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="phones"
    )

    class Meta:
        db_table = "users_phones"


# -----------------EMPLOYEE----------------


class Employee(BaseModel):

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    role = models.PositiveSmallIntegerField(
        choices=EmployeeType, default=EmployeeType.COOKER
    )

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="employee",
    )

    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="employee"
    )

    class Meta:
        db_table = "users_employees"


# -----------------CUSTOMER----------------


class Customer(BaseModel):

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    role = models.PositiveSmallIntegerField(
        choices=CustomerType, default=CustomerType.GUEST
    )

    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="customer"
    )

    account = models.OneToOneField(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customer",
    )

    class Meta:
        db_table = "users_customers"


class LoyaltyPoint(BaseModel):

    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, related_name="loyalty"
    )

    points = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "users_loyalty_points"

    def clean(self):
        if not self.customer.account:
            raise ValidationError(
                "Cannot create loyalty points for customer without account"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
