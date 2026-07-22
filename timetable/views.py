from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.decorators import admin_or_teacher
from .models import Timetable
from .forms import TimetableForm


@login_required
def timetable_list(request):

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