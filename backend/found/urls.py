from django.urls import path
from . import views

urlpatterns=[
    path("latest/", views.latestFound),
    path("new/", views.newItem),
    path("userfound/", views.markUserFound),
    path("<id>/", views.getItem),
    path("latest", views.latestFound),
    path("new", views.newItem),
    path("userfound", views.markUserFound),
    path("<id>", views.getItem)
]