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
from rest_framework.viewsets import ModelViewSet


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product__id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'product can not be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
            count_product=Count('product')
        )
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if Product.objects.filter(collection__id=instance.id).count() > 0:
            print(Product.objects.filter(collection__id=instance.id).count())
            return Response({'error': 'collection can not be deleted'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return Response({}, status=status.HTTP_204_NO_CONTENT)








