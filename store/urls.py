from django.urls import path
from .views import *



urlpatterns = [
    path('products/', ProductList.as_view()),
    path('products/<int:pk>', ProductDetail.as_view()),
    path('collection/', CollectionList.as_view()),
    path('collection/<int:pk>', CollectionDetail.as_view()),
]