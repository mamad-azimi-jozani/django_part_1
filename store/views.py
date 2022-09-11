from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import *
from rest_framework import status
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView


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
            return Response({'error': 'product can not be deleted'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        instance.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {
            'product_id': self.kwargs['product_pk']
        }





