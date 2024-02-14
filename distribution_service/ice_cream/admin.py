from django.contrib import admin

from ice_cream.models import IceCreamItem, IceCream

admin.site.register(IceCream)
admin.site.register(IceCreamItem)
