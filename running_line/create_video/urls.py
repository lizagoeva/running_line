from django.urls import path
from .views import index_page, create_video, show_database

app_name = 'create_video'
urlpatterns = [
    path('', index_page, name='init_page'),
    path('create-video', create_video, name='create_video'),
    path('show-database/', show_database, name='show_database'),
]
