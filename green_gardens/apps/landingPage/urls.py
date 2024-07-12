from django.urls import path
from . import views

app_name = 'landingPage'
urlpatterns = [
    path('', views.index, name='index'),
    path('download', views.download_ebook, name='download-ebook'),
]