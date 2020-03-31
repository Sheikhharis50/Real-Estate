from django.urls import path

from . import views

urlpatterns = [
    # define routes for pages here 
    path('', views.index, name='index'),
    path('about', views.about, name='about')
]