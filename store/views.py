from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer, CollectionSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import *
from rest_framework import status
from django.db.models import Count
from django.shortcuts import get_object_or_404
class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        if product.orderitem_set.count() > 0:
            return Response({'error': 'product can not be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
            count_product=Count('product')
        )
    serializer_class = CollectionSerializer


# class CollectionDetail(RetrieveUpdateDestroyAPIView):

class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(
        count_product=Count('product'))
    serializer_class = CollectionSerializer
    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.product_set.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)



# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, id):
#     collection = get_object_or_404(Collection.objects.annotate(
#         count_product=Count('product')), id=id)
#
#
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)
#     elif request.method == 'DELETE':
#         serializer = CollectionSerializer(collection)
