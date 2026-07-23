from courses.models import Course
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import admin_or_teacher
from .models import Fee
from .forms import FeeForm


@login_required
def fee_list(request):

    query = request.GET.get("q")

    if request.user.is_superuser or request.user.profile.role in ["Admin", "Teacher"]:

        fees = Fee.objects.select_related(
            "student",
            "course"
        )

        if query:
            fees = fees.filter(
                student__username__icontains=query
            )

    else:

        fees = Fee.objects.filter(
            student=request.user
        ).select_related(
            "student",
            "course"
        )

    return render(
        request,
        "fees/fee_list.html",
        {
            "fees": fees
        }
    )


@login_required
@admin_or_teacher
def add_fee(request):

    if request.method == "POST":

        form = FeeForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("fee_list")

    else:

        form = FeeForm()

    return render(
        request,
        "fees/add_fee.html",
        {
            "form": form
        }
    )


@login_required
@admin_or_teacher
def edit_fee(request, id):

    fee = get_object_or_404(
        Fee,
        id=id
    )

    if request.method == "POST":

        form = FeeForm(
            request.POST,
            instance=fee
        )

        if form.is_valid():

            form.save()

            return redirect("fee_list")

    else:

        form = FeeForm(
            instance=fee
        )

    return render(
        request,
        "fees/add_fee.html",
        {
            "form": form
        }
    )


@login_required
@admin_or_teacher
def delete_fee(request, id):

    fee = get_object_or_404(
        Fee,
        id=id
    )

    fee.delete()

    return redirect("fee_list")

@login_required
def class_fees(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    fees = Fee.objects.filter(
        course=course
    ).select_related(
        "student",
        "course"
    )

    return render(
        request,
        "fees/fee_list.html",
        {
            "fees": fees,
            "course": course,
        }
    )