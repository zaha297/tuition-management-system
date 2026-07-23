from django.urls import path
from . import views

urlpatterns = [
    path("", views.attendance_list, name="attendance_list"),
path("class/<int:course_id>/", views.class_attendance, name="class_attendance"),
    path("add/", views.add_attendance, name="add_attendance"),
    path("edit/<int:id>/", views.edit_attendance, name="edit_attendance"),
    path("delete/<int:id>/", views.delete_attendance, name="delete_attendance"),
]