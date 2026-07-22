from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.decorators import admin_or_teacher
from .models import Course, Enrollment
from .forms import CourseForm, EnrollmentForm


# ======================================
# COURSE LIST
# ======================================

@login_required
def course_list(request):

    query = request.GET.get("q")

    if query:
        courses = Course.objects.filter(
            course_name__icontains=query
        )
    else:
        courses = Course.objects.all()

    return render(
        request,
        "courses/course_list.html",
        {
            "courses": courses
        }
    )


# ======================================
# ADD COURSE
# ======================================

@login_required
@admin_or_teacher
def add_course(request):

    if request.method == "POST":

        form = CourseForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("course_list")

    else:

        form = CourseForm()

    return render(
        request,
        "courses/add_course.html",
        {
            "form": form
        }
    )


# ======================================
# EDIT COURSE
# ======================================

@login_required
@admin_or_teacher
def edit_course(request, id):

    course = get_object_or_404(
        Course,
        id=id
    )

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            instance=course
        )

        if form.is_valid():

            form.save()

            return redirect("course_list")

    else:

        form = CourseForm(
            instance=course
        )

    return render(
        request,
        "courses/add_course.html",
        {
            "form": form
        }
    )


# ======================================
# DELETE COURSE
# ======================================

@login_required
@admin_or_teacher
def delete_course(request, id):

    course = get_object_or_404(
        Course,
        id=id
    )

    course.delete()

    return redirect("course_list")


# ======================================
# ENROLLMENT LIST
# ======================================

@login_required
def enrollment_list(request):

    enrollments = Enrollment.objects.select_related(
        "student",
        "course"
    )

    return render(
        request,
        "courses/enrollment_list.html",
        {
            "enrollments": enrollments
        }
    )


# ======================================
# ADD ENROLLMENT
# ======================================

@login_required
@admin_or_teacher
def add_enrollment(request):

    if request.method == "POST":

        form = EnrollmentForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("enrollment_list")

    else:

        form = EnrollmentForm()

    return render(
        request,
        "courses/add_enrollment.html",
        {
            "form": form
        }
    )


# ======================================
# EDIT ENROLLMENT
# ======================================

@login_required
@admin_or_teacher
def edit_enrollment(request, id):

    enrollment = get_object_or_404(
        Enrollment,
        id=id
    )

    if request.method == "POST":

        form = EnrollmentForm(
            request.POST,
            instance=enrollment
        )

        if form.is_valid():

            form.save()

            return redirect("enrollment_list")

    else:

        form = EnrollmentForm(
            instance=enrollment
        )

    return render(
        request,
        "courses/add_enrollment.html",
        {
            "form": form
        }
    )


# ======================================
# DELETE ENROLLMENT
# ======================================

@login_required
@admin_or_teacher
def delete_enrollment(request, id):

    enrollment = get_object_or_404(
        Enrollment,
        id=id
    )

    enrollment.delete()

    return redirect("enrollment_list")