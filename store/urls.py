from django.urls import path
from .views import *



urlpatterns = [
    path('products/', ProductList.as_view()),
    path('products/<int:id>', ProductDetail.as_view()),
    path('collection/', collection_list),
    path('collection/<int:id>', collection_detail),
]