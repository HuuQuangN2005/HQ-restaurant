from django.db import models
from django.core.validators import MinValueValidator

from restaurant.models import UUIDBaseModel
from products.models import Food
from users.models import Account, Address


class ReservationStatus(models.IntegerChoices):
    PENDING = 1
    ACCEPTED = 2
    DENIED = 3


class OrderStatus(models.IntegerChoices):
    PENDING = 1
    COMPLETED = 2
    CANCELLED = 3


class Interaction(UUIDBaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=False)

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.content

    class Meta:
        db_table = "actions_comments"


class Reservation(UUIDBaseModel):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="reservations"
    )
    date = models.DateTimeField(null=False, blank=False)

    participants = models.PositiveIntegerField(
        null=False, blank=False, validators=[MinValueValidator(1)], default=1
    )

    note = models.TextField(null=True, blank=True)

    status = models.PositiveSmallIntegerField(
        choices=ReservationStatus.choices, default=ReservationStatus.PENDING
    )

    class Meta:
        db_table = "actions_reservations"


class Order(UUIDBaseModel):
    account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name="orders"
    )
    address = models.ForeignKey(
        Address, on_delete=models.PROTECT, null=True, blank=True
    )
    status = models.PositiveSmallIntegerField(
        choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    total_price = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, validators=[MinValueValidator(0)]
    )
    is_paid = models.BooleanField(default=False)

    note = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "actions_orders"


class OrderDetail(UUIDBaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="details")
    food = models.ForeignKey(
        Food, on_delete=models.PROTECT, related_name="order_details"
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=15, decimal_places=2, validators=[MinValueValidator(0)]
    )

    def save(self, *args, **kwargs):
        if not self.price and self.food:
            self.price = self.food.price

        super().save(*args, **kwargs)

    class Meta:
        db_table = "actions_order_details"
