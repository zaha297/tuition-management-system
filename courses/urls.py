from django.urls import path
from . import views

urlpatterns = [

    # My Classes
    path("my-classes/", views.my_classes, name="my_classes"),

    # Course URLs
    path("", views.course_list, name="course_list"),
    path("add/", views.add_course, name="add_course"),
    path("edit/<int:id>/", views.edit_course, name="edit_course"),
    path("delete/<int:id>/", views.delete_course, name="delete_course"),

    # Enrollment URLs
    path("enrollments/", views.enrollment_list, name="enrollment_list"),
    path("enrollments/add/", views.add_enrollment, name="add_enrollment"),
    path("enrollments/edit/<int:id>/", views.edit_enrollment, name="edit_enrollment"),
    path("enrollments/delete/<int:id>/", views.delete_enrollment, name="delete_enrollment"),
    path("class/<int:id>/", views.class_detail, name="class_detail"),
    path("class/<int:id>/", views.class_detail, name="class_detail"),
    path("class/<int:id>/students/", views.class_students, name="class_students"),
]