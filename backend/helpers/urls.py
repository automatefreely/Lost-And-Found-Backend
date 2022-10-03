from django.urls import path
from . import views

urlpatterns=[
    path("auth/", views.authUser),
    path("self/", views.getSelfUser),
    path("uploadimage/", views.imageUpload)
]