from django.db import models
from django.core.validators import MinValueValidator
import uuid
from helper.model import Meta


class IceCream(Meta):
    """
    The IceCream model, inheriting from Meta,
    represents ice cream products with attributes including title,
    a unique UUID slug, flavor, description, and price. It's
    designed to comprehensively capture product details,
    facilitating inventory management and sales operations.
    The model ensures each product can be uniquely identified and described,
    supporting functionalities like cataloging and eCommerce transactions.
    The unique_together constraint on title and UUID slug ensures product
    uniqueness within the database, preventing duplicate entries and maintaining data integrity.
    """
    title = models.CharField(max_length=300, help_text='Product title.')
    uuid_slug = models.UUIDField(
        default=uuid.uuid4, db_index=True, help_text='unique uuid identifier for the product')
    flavor = models.CharField(
        max_length=100, default='chocolate', help_text='Ice cream flavour')
    description = models.TextField(
        max_length=500, help_text='Product description.')
    price = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)], help_text='Product price')

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.title}"

    class Meta(Meta.Meta):
        unique_together = [("title", "uuid_slug")]


class IceCreamItem(Meta):
    """
    The IceCreamItem model extends the Meta class, serving as a bridge
     between IceCream products and their quantities in various contexts,
     such as orders or carts. It links to the IceCream model via a foreign key,
     ensuring each item is associated with a specific ice cream flavor.
     The quantity field tracks the number of units for the associated product,
     facilitating inventory and order management. This model is essential for
     representing individual product selections and their respective quantities
     within the system.
    """
    ice_cream = models.ForeignKey(
        IceCream, related_name='ice_cream_item', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.ice_cream.title}"
