from django.urls import path
from . import views

urlpatterns=[
    path("latest/", views.latestLost),
    path("new/", views.newItem),
    path("found/", views.markFound),
    path("<id>/", views.getItem)
]