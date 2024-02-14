from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
import logging

from ice_cream.models import IceCream

logger = logging.getLogger(__name__)


@login_required
def ice_cream_list(request):
    products = cache.get('ice_cream_products')
    if not products:
        products = IceCream.objects.all()
        cache.set('ice_cream_products', products,
                  timeout=3600)  # Cache for 1 hour
    return render(request, 'products/ice_cream_list.html', {'products': products})
