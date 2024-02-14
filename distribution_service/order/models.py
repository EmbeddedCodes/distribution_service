from django.db import models
from django.contrib.auth import get_user_model

from ice_cream.models import Meta, IceCream, IceCreamItem

User = get_user_model()


class Order(Meta):
    """
    This Django model class represents an order in the system, 
    uniquely identified by an order_number and linked to the user who created it. 
    It tracks the order's status through various stages, 
    from creation to completion, and associates multiple IceCream items with each order. 
    The total field calculates the overall cost. 
    Additional details specific to the order can be stored in the content field. 
    This model also includes methods to retrieve total orders, filter orders by ice cream flavor, 
    and calculate the average order value, facilitating comprehensive order management and analysis.
    """
    order_number = models.BigIntegerField(
        unique=True, default=1001, help_text="Unique number to identify the order")
    created_by = models.ForeignKey(
        User, related_name="order", on_delete=models.DO_NOTHING, null=True, help_text="The user created this order")
    status = models.CharField(max_length=30, default='unpaid',
                              help_text='The status of the order can be Paid, unpaid. Other status like Failed, Shipped, \
                              Delivered, Returned, and Complete can be used accordingly.')
    items = models.ManyToManyField(
        IceCream, related_name='order', blank=True, help_text="The items associated with the order.")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                help_text='The total price of the Order.')
    content = models.CharField(max_length=500, default='', blank=True,
                               help_text='Additional details of the order.')

    def __str__(self):
        return f"order {self.order_number} for {self.created_by.username}"

    class Meta(Meta.Meta):
        unique_together = [("order_number", "status")]

    @classmethod
    def get_total_orders(cls):
        return cls.objects.count()

    @classmethod
    def get_orders_by_flavor(cls, flavor):
        return cls.objects.filter(items__ice_cream__flavor=flavor)

    @classmethod
    def get_average_order_value(cls):
        return cls.objects.annotate(order_value=models.F('total')).aggregate(models.Avg('order_value'))


class Cart(Meta):
    """
    The Cart model, inheriting from Meta, is designed to represent a user's shopping cart
    in the system. It establishes a one-to-one relationship with the User model, 
    ensuring each user has a unique cart. The cart can contain multiple IceCreamItem instances, 
    allowing users to add various ice cream items to their cart. 
    This model is key to managing the shopping cart functionality within the application, 
    offering a straightforward way to track user selections before purchase.
    """
    user = models.OneToOneField(
        User, related_name='cart', on_delete=models.CASCADE, help_text='cart owner.')
    items = models.ManyToManyField(
        IceCreamItem, related_name='cart', help_text='Items added to the cart.')

    def __str__(self) -> str:
        return f"Cart for {self.user.username}"
