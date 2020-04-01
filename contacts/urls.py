from django.urls import path

from . import views

urlpatterns = [
    # define routes for pages here
    path('contact', views.contact, name='contact'),
]
