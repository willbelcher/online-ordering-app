from django.db import models

class OrderStatuses(models.IntegerChoices):
    IN_PROGRESS = 1, "In Progress"
    SUBMITTED = 2, "Submitted"
    ACCEPTED = 3, "Accepted"
    COMPLETED = 4, "Completed"

class MenuItem(models.Model):
    name = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    available = models.BooleanField(default=True)

class Order(models.Model):
    user = models.TextField(max_length=35, null=True)
    store = models.IntegerField()
    status = models.IntegerField(choices=OrderStatuses.choices, default=OrderStatuses.IN_PROGRESS)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING) # Test change to cascade

