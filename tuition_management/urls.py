from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [

    path("", home, name="home"),

    path("admin/", admin.site.urls),

    path("", include("users.urls")),

    path("courses/", include("courses.urls")),

    path("attendance/", include("attendance.urls")),

    path("fees/", include("fees.urls")),

    path("timetable/", include("timetable.urls")),

    path("assignments/", include("assignments.urls")),

    path("notices/", include("noticeboard.urls")),
]