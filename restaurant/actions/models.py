from django.db import models

from restaurant.models import UUIDBaseModel
from products.models import Food
from users.models import Account

class Interaction(UUIDBaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=False)

    class Meta:
        abstract = True

class Comment(Interaction):
    content = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.content


class Like(Interaction):
    class Meta:
        unique_together = ('account', 'food')