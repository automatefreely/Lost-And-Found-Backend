from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.getAllCategories),
    path("categories", views.getAllCategories),
    path("", views.getAllTags)
]
