from django.urls import path
from . import views

urlpatterns=[
    path("auth", views.auth_user),
    path("self", views.get_self)
]