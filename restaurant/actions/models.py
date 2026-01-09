from django.db import models
from django.core.validators import MinValueValidator

from restaurant.models import UUIDBaseModel
from products.models import Food
from users.models import Account


class ReservationStatus(models.IntegerChoices):
    PENDING = 1
    ACCEPTED = 2
    DENIED = 3


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
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)
    date = models.DateTimeField(null=False, blank=False)
    
    participants = models.PositiveIntegerField(
        null=False, 
        blank=False,
        validators=[MinValueValidator(1)],
        default=1
    )
    
    notes = models.TextField(null=True, blank=True)
    
    status = models.PositiveSmallIntegerField(
        choices=ReservationStatus.choices, 
        default=ReservationStatus.PENDING
    )

    class Meta:
        db_table = "actions_reservations"
        
        
