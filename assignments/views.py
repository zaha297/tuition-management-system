from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.decorators import admin_or_teacher
from .models import Assignment
from .forms import AssignmentForm


@login_required
def assignment_list(request):

    query = request.GET.get("q")

    assignments = Assignment.objects.select_related(
        "course"
    )

    if query:

        assignments = assignments.filter(
            title__icontains=query
        )

    return render(
        request,
        "assignments/assignment_list.html",
        {
            "assignments": assignments
        }
    )


@login_required
@admin_or_teacher
def add_assignment(request):

    if request.method == "POST":

        form = AssignmentForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("assignment_list")

    else:

        form = AssignmentForm()

    return render(
        request,
        "assignments/add_assignment.html",
        {
            "form": form
        }
    )


@login_required
@admin_or_teacher
def edit_assignment(request, id):

    assignment = get_object_or_404(
        Assignment,
        id=id
    )

    if request.method == "POST":

        form = AssignmentForm(
            request.POST,
            instance=assignment
        )

        if form.is_valid():

            form.save()

            return redirect("assignment_list")

    else:

        form = AssignmentForm(
            instance=assignment
        )

    return render(
        request,
        "assignments/add_assignment.html",
        {
            "form": form
        }
    )


@login_required
@admin_or_teacher
def delete_assignment(request, id):

    assignment = get_object_or_404(
        Assignment,
        id=id
    )

    assignment.delete()

    return redirect("assignment_list")