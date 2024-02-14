from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from django.core.cache import cache
import logging

from ice_cream.api.serializers import IceCreamSerializer, IceCreamRequestSerializer
from ice_cream.models import IceCream

logger = logging.getLogger(__name__)


@extend_schema(
    request=None,
    responses={status.HTTP_200_OK: IceCreamSerializer(many=True)},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_products(request):
    """
        Returns all saved products,
        Authentication not required.
    """

    products = cache.get('ice_cream_products')
    if not products:
        products = IceCream.objects.all()
        cache.set('ice_cream_products', products,
                  timeout=3600)
    serializer = IceCreamSerializer(products, many=True)

    return Response(serializer.data)


@extend_schema(
    request=IceCreamRequestSerializer,
    responses={status.HTTP_201_CREATED: IceCreamSerializer},
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_product(request):
    """
        Creat new product, only admin user is allowed to perform this action.
        Request body:
        {
        "title": "string",
        "flavor": "string",
        "description": "string",
        "price": "45"
        }
    """
    serializer = IceCreamRequestSerializer(data=request.data)
    if serializer.is_valid():
        product = serializer.save()
        response_serializer = IceCreamSerializer(product)
        logger.info(f"Product with id: {product.id} has been added")
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=None,
    responses={status.HTTP_204_NO_CONTENT: None},
)
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_product(request, product_id):
    """
        Delete existing product, only admin user is allowed to perform this action.

        product_id is required
    """
    product = get_object_or_404(IceCream, id=product_id)
    product.delete()
    logger.info(f"Product with id: {product_id} has been deleted")

    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    request=IceCreamRequestSerializer,
    responses={status.HTTP_200_OK: IceCreamSerializer},
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def update_product(request, product_id):
    """
        Update product details, only admin user is allowed to perform this action.
        product_id is required

    """

    product = get_object_or_404(IceCream, id=product_id)
    serializer = IceCreamRequestSerializer(
        product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        logger.info(f"Product with id: {product_id} has been updated")
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
