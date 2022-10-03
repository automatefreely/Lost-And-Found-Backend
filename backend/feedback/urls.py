from django.urls import path
from . import views

urlpatterns=[
    path("latest/", views.getFeedbacks),
    path("new/", views.newFeedback),
    path("latest", views.getFeedbacks),
    path("new", views.newFeedback),
]