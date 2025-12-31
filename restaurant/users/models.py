from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import transaction
from uuid import uuid4

from cloudinary.models import CloudinaryField


class Gender(models.IntegerChoices):
    MALE = 1, "male"
    FEMALE = 2, "female"
    OTHER = 3, "other"


class UserRole(models.IntegerChoices):
    ADMIN = 1, "admin"
    COOKER = 2, "cooker"
    CUSTOMER = 3, "customer"


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Email(BaseModel):
    account = models.ForeignKey(
        "Account", on_delete=models.CASCADE, related_name="emails"
    )
    email = models.EmailField(unique=True)
    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.is_primary:
            Email.objects.filter(account=self.account, is_primary=True).exclude(
                id=self.id
            ).update(is_primary=False)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "users_emails"


class AccountManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")

        with transaction.atomic():
            account = self.model(username=username, **extra_fields)
            account.set_password(password)
            account.save(using=self._db)

            Email.objects.create(
                account=account,
                email=self.normalize_email(email),
                is_primary=True,
                is_verified=False,
            )

        return account

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin, BaseModel):

    username = models.CharField(max_length=150, unique=True, db_index=True)

    avatar = CloudinaryField

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    @property
    def email(self):
        primary_email = self.emails.filter(is_primary=True).first()
        return primary_email.email if primary_email else ""

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users_accounts"


class BaseUserProfile(BaseModel):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    gender = models.PositiveSmallIntegerField(
        choices=Gender.choices, default=Gender.OTHER
    )

    role = models.PositiveSmallIntegerField(
        choices=UserRole.choices, default=UserRole.CUSTOMER
    )

    def __str__(self):
        return self.uuid

    class Meta:
        abstract = True


class Employee(BaseUserProfile):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="employee_profile"
    )
    employee_code = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    start_date = models.DateField()

    class Meta:
        db_table = "users_employees"


class Customer(BaseUserProfile):
    account = models.OneToOneField(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customer_profile",
    )
    loyalty_points = models.IntegerField(default=0)
    is_vip = models.BooleanField(default=False)

    class Meta:
        db_table = "users_customers"
