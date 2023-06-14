from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

class OrderStatuses(models.IntegerChoices):
    IN_PROGRESS = 1, "In Progress"
    SUBMITTED = 2, "Submitted"
    ACCEPTED = 3, "Accepted"
    COMPLETED = 4, "Completed"

class BusinessHours(models.Model):
    mon_open = models.TimeField(null=True)
    mon_close = models.TimeField(null=True)

    tue_open = models.TimeField(null=True)
    tue_close = models.TimeField(null=True)

    wed_open = models.TimeField(null=True)
    wed_close = models.TimeField(null=True)

    thu_open = models.TimeField(null=True)
    thu_close = models.TimeField(null=True)

    fri_open = models.TimeField(null=True)
    fri_close = models.TimeField(null=True)

    sat_open = models.TimeField(null=True)
    sat_close = models.TimeField(null=True)

    sun_open = models.TimeField(null=True)
    sun_close = models.TimeField(null=True)

class MenuItem(models.Model):
    name = models.TextField(max_length=15)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    available = models.BooleanField(default=True)

class Store(models.Model):
    name = models.TextField(max_length=75)
    # location = None
    address = models.TextField(max_length=150)
    schedule = models.OneToOneField(BusinessHours, on_delete=models.CASCADE)
    out_of_schedule_close = models.BooleanField(default=False)
    available_items = models.ManyToManyField(MenuItem)

class Order(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, null=False, on_delete=models.DO_NOTHING) # test change
    status = models.PositiveSmallIntegerField(choices=OrderStatuses.choices, default=OrderStatuses.IN_PROGRESS)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING) # Test change to cascade
    quantity = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(15, "Maximum quantity reached")])