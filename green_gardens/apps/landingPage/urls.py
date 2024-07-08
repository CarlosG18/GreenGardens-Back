from django.urls import path
from . import views

app_name = 'landingPage'
urlpatterns = [
    path('', views.index, name='index'),
    path('dinamic-styles', views.dynamic_css_view, name="dinamic_styles"),
    path('download-ebook/', views.download_ebook, name="download_ebook"),
]