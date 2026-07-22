from django.urls import path
from . import views

urlpatterns = [
    path("", views.fee_list, name="fee_list"),
    path("add/", views.add_fee, name="add_fee"),
    path("edit/<int:id>/", views.edit_fee, name="edit_fee"),
    path("delete/<int:id>/", views.delete_fee, name="delete_fee"),
]