from django.urls import path
from .views import create_video

app_name = 'create_video'
urlpatterns = [
    path('', create_video, name='create_video'),
    # path('products/', products_list, name='products_list'),
    # path('orders/', orders_list, name='orders_list'),
]
