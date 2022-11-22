from django.urls import path
from . import views



urlpatterns = [
    path("", views.download_vedio,name="home"),
    
]
