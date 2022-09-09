from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer, CollectionSerializer
from rest_framework.generics import ListCreateAPIView
from .models import *
from rest_framework import status
from django.db.models import Count
from django.shortcuts import get_object_or_404
class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(APIView):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        if request.method == 'GET':
            serializer = ProductSerializer(product)
            return Response(serializer.data)
    def put(self, request, id):
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, id):
        product = Product.objects.get(id=id)
        if product.orderitem_set.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
            count_product=Count('product')
        )
    serializer_class = CollectionSerializer


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == "GET":
        queryset = Collection.objects.annotate(
            count_product=Count('product')
        )
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, id):
    collection = get_object_or_404(Collection.objects.annotate(
        count_product=Count('product')), id=id)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        serializer = CollectionSerializer(collection)
        if collection.product_set.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)