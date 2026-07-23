from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.decorators import admin_or_teacher
from .models import Timetable
from .forms import TimetableForm
from courses.models import Course
from .models import Timetable


@login_required
def class_timetable(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    timetable = Timetable.objects.filter(course=course)

    return render(
        request,
        "timetable/class_timetable.html",
        {
            "course": course,
            "timetable": timetable,
        }
    )


@login_required
def timetable_list(request):

    # Admin can see everything
    if request.user.is_superuser:
        timetables = Timetable.objects.select_related("course")

    else:

        profile = request.user.profile

        if profile.role == "Student":

            enrollments = request.user.enrollment_set.all()

            course_ids = enrollments.values_list(
                "course_id",
                flat=True
            )

            timetables = Timetable.objects.filter(
                course_id__in=course_ids
            ).select_related("course")

        else:

            timetables = Timetable.objects.select_related("course")

    return render(
        request,
        "timetable/timetable_list.html",
        {
            "timetables": timetables
        }
    )

@login_required
@admin_or_teacher
def add_timetable(request):

    if request.method == "POST":

        form = TimetableForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("timetable_list")

    else:

        form = TimetableForm()

    return render(
        request,
        "timetable/add_timetable.html",
        {
            "form": form
        }
    )


@login_required
@admin_or_teacher
def edit_timetable(request, id):

    entry = get_object_or_404(Timetable, id=id)

    if request.method == "POST":

        form = TimetableForm(
            request.POST,
            instance=entry
        )

        if form.is_valid():

            form.save()

            return redirect("timetable_list")

    else:

        form = TimetableForm(
            instance=entry
        )

    return render(
        request,
        "timetable/add_timetable.html",
        {
            "form": form
        }
    )


@login_required
@admin_or_teacher
def delete_timetable(request, id):

    entry = get_object_or_404(
        Timetable,
        id=id
    )

    entry.delete()

    return redirect("timetable_list")