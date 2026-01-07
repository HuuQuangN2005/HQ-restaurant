from django.db import models
from users.models import Account, Address
from products.models import Food
from django.core.validators import MinValueValidator
from uuid import uuid4


class UUIDBaseModel(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, db_index=True, editable=False)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OrderStatus(models.IntegerChoices):
    PENDING = 1
    ACCEPTED = 2
    COMPLETED = 3
    CANCELLED = 4


class Order(UUIDBaseModel):
    customer = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="orders"
    )
    address = models.ForeignKey(
        Address, on_delete=models.PROTECT, null=True, blank=True
    )
    status = models.PositiveSmallIntegerField(
        choices=OrderStatus.choices, default=OrderStatus.PENDING
    )

    total_price = models.DecimalField(
        max_digits=20, decimal_places=2, validators=[MinValueValidator(0)], default=0
    )
    is_paid = models.BooleanField(default=False)

    class Meta:
        db_table = "orders_orders"
        ordering = ["-created_date"]


class OrderDetail(UUIDBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="details")
    food = models.ForeignKey(
        Food, on_delete=models.PROTECT, related_name="order_details"
    )
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)]
    )

    unit_price = models.DecimalField(
        max_digits=15, decimal_places=2, validators=[MinValueValidator(0)]
    )
    note = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.food.price
        super().save(*args, **kwargs)

    class Meta:
        db_table = "orders_details"
