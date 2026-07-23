from django.urls import path
from . import views

urlpatterns = [

    path("", views.assignment_list, name="assignment_list"),

    path("add/", views.add_assignment, name="add_assignment"),

    path("edit/<int:id>/", views.edit_assignment, name="edit_assignment"),

    path("delete/<int:id>/", views.delete_assignment, name="delete_assignment"),

    path("class/<int:course_id>/", views.class_assignments, name="class_assignments"),
]