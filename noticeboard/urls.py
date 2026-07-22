from django.urls import path
from . import views

urlpatterns = [

    path("", views.notice_list, name="notice_list"),

    path("add/", views.add_notice, name="add_notice"),

    path("edit/<int:id>/", views.edit_notice, name="edit_notice"),

    path("delete/<int:id>/", views.delete_notice, name="delete_notice"),

]