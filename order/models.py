from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class OrderStatuses(models.IntegerChoices):
    IN_PROGRESS = 1, "In Progress"
    SUBMITTED = 2, "Submitted"
    ACCEPTED = 3, "Accepted"
    COMPLETED = 4, "Completed"

class OrderMethods(models.TextChoices):
    PICKUP = "Pickup"
    DELIVERY = "Delivery"

# order of fields here currently determines order displayed
class MenuItemCategories(models.TextChoices):
    APPETIZER = "Appetizer"
    SALAD = "Salad"
    PIZZA = "Pizza"

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

class OrderMethod(models.Model):
    method = models.TextField(choices=OrderMethods.choices, default=OrderMethods.PICKUP, unique=True)

class Address(models.Model):
    street = models.CharField(max_length=45, blank=False)
    city = models.CharField(max_length=30, blank=False)
    state = models.CharField(max_length=2, blank=False)
    zipcode = models.CharField(max_length=5, blank=False)

    def __str__(self):
        return f"{self.street}\n{self.city}, {self.state} {self.zipcode}"

class MenuItem(models.Model):
    name = models.CharField(max_length=15, unique=True)
    category = models.TextField(choices=MenuItemCategories.choices, default=MenuItemCategories.PIZZA)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    ingredients = models.TextField(max_length=255, blank=True)
    available = models.BooleanField(default=True)

class Store(models.Model):
    name = models.CharField(max_length=75, unique=True)
    # location = None
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    timezone = models.CharField(default="UTC", max_length=30)
    schedule = models.OneToOneField(BusinessHours, on_delete=models.CASCADE)
    out_of_schedule_close = models.BooleanField(default=False)
    available_items = models.ManyToManyField(MenuItem, related_name="stores_where_available")
    order_methods = models.ManyToManyField(OrderMethod)

class Order(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="orders")
    store = models.ForeignKey(Store, null=False, on_delete=models.DO_NOTHING, related_name="orders") # test change
    order_method = models.ForeignKey(OrderMethod, null=False, on_delete=models.DO_NOTHING) # test change
    status = models.PositiveSmallIntegerField(choices=OrderStatuses.choices, default=OrderStatuses.IN_PROGRESS)
    date_created = models.DateTimeField(auto_now_add=True, editable=False, blank=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING) # Test change to cascade
    quantity = models.PositiveSmallIntegerField(default=1, validators=[MaxValueValidator(15, "Maximum quantity reached")])
    special_instructions = models.TextField(max_length=255, blank=True)