from django.db import models


class GenderType(models.IntegerChoices):
    MALE = 1, "male"
    FEMALE = 2, "female"
    OTHER = 3, "other"


class EmployeeType(models.IntegerChoices):
    ADMIN = 1, "admin"
    COOKER = 2, "cooker"


class CustomerType(models.IntegerChoices):
    GUEST = 1, "guest"
    MEMBER = 2, "member"
