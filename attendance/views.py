from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import admin_or_teacher
from .models import Attendance
from .forms import AttendanceForm


@login_required
def attendance_list(request):

    query = request.GET.get("q")

    attendances = Attendance.objects.select_related(
        "student",
        "course"
    )

    if query:

        attendances = attendances.filter(
            student__username__icontains=query
        )

    return render(
        request,
        "attendance/attendance_list.html",
        {
            "attendances": attendances
        }
    )


@login_required
@admin_or_teacher
def add_attendance(request):

    if request.method == "POST":

        form = AttendanceForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("attendance_list")

    else:

        form = AttendanceForm()

    return render(
        request,
        "attendance/add_attendance.html",
        {
            "form": form
        }
    )


@login_required
@admin_or_teacher
def edit_attendance(request, id):

    attendance = get_object_or_404(
        Attendance,
        id=id
    )

    if request.method == "POST":

        form = AttendanceForm(
            request.POST,
            instance=attendance
        )

        if form.is_valid():

            form.save()

            return redirect("attendance_list")

    else:

        form = AttendanceForm(
            instance=attendance
        )

    return render(
        request,
        "attendance/add_attendance.html",
        {
            "form": form
        }
    )


@login_required
@admin_or_teacher
def delete_attendance(request, id):

    attendance = get_object_or_404(
        Attendance,
        id=id
    )

    attendance.delete()

    return redirect("attendance_list")