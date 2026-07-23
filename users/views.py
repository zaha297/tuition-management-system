from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .forms import UserRegisterForm, StudentForm, TeacherForm
from .models import Profile
from .decorators import admin_or_teacher

from timetable.models import Timetable
from courses.models import Course, Enrollment
from attendance.models import Attendance
from fees.models import Fee
from assignments.models import Assignment


# =====================================================
# REGISTER
# =====================================================

def register(request):

    if request.method == "POST":

        form = UserRegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            Profile.objects.create(
                user=user,
                role=form.cleaned_data["role"]
            )

            login(request, user)

            return redirect("dashboard")

    else:

        form = UserRegisterForm()

    return render(
        request,
        "users/register.html",
        {
            "form": form
        }
    )


# =====================================================
# LOGIN
# =====================================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        return render(
            request,
            "users/login.html",
            {
                "error": "Invalid Username or Password"
            }
        )

    return render(
        request,
        "users/login.html"
    )


# =====================================================
# ROLE LOGIN PAGES
# =====================================================

def teacher_login(request):
    return render(request, "users/teacher_login.html")


def student_login(request):
    return render(request, "users/student_login.html")


def parent_login(request):
    return render(request, "users/parent_login.html")


def admin_login(request):
    return render(request, "users/admin_login.html")


# =====================================================
# LOGOUT
# =====================================================

@login_required
def logout_view(request):

    logout(request)

    return redirect("home")
    # =====================================================
# DASHBOARD
# =====================================================

@login_required
def dashboard(request):

    context = {

        "course_count": Course.objects.count(),
        "attendance_count": Attendance.objects.count(),
        "fee_count": Fee.objects.count(),

        "student_count": Profile.objects.filter(
            role="Student"
        ).count(),

        "teacher_count": Profile.objects.filter(
            role="Teacher"
        ).count(),

        
        "recent_students": Profile.objects.filter(
            role="Student"
        ).select_related("user").order_by("-id")[:5],

        "recent_courses": Course.objects.order_by("-id")[:5],

        "recent_attendance": Attendance.objects.select_related(
            "student",
            "course"
        ).order_by("-id")[:5],

        "recent_fees": Fee.objects.select_related(
            "student",
            "course"
        ).order_by("-id")[:5],
    }

    # -------------------------------
    # SUPER ADMIN
    # -------------------------------

    if request.user.is_superuser:

        return render(
            request,
            "users/admin_dashboard.html",
            context
        )

    # -------------------------------
    # GET PROFILE
    # -------------------------------

    try:

        profile = Profile.objects.get(
            user=request.user
        )

    except Profile.DoesNotExist:

        logout(request)

        return redirect("login")

    # -------------------------------
    # TEACHER
    # -------------------------------

    if profile.role == "Teacher":

        courses = Course.objects.filter(
            teacher=request.user
        )

        context["courses"] = courses

        return render(
            request,
            "users/teacher_dashboard.html",
            context
        )

    # -------------------------------
    # STUDENT
    # -------------------------------

    elif profile.role == "Student":

        student = request.user

        context["my_attendance"] = Attendance.objects.filter(
            student=student
        ).order_by("-date")[:5]

        context["my_fees"] = Fee.objects.filter(
            student=student
        ).order_by("-payment_date")[:5]

        enrollments = Enrollment.objects.filter(
            student=student
        ).select_related("course")

        my_courses = []

        for enrollment in enrollments:
            my_courses.append(enrollment.course)

        context["my_courses"] = my_courses

        course_ids = []

        for course in my_courses:
            course_ids.append(course.id)

        context["my_assignments"] = Assignment.objects.filter(
            course__id__in=course_ids
        ).order_by("due_date")[:5]

        context["my_timetable"] = Timetable.objects.filter(
            course__id__in=course_ids
        ).order_by("day", "start_time")[:5]

        context["student_profile"] = profile

        return render(
            request,
            "users/student_dashboard.html",
            context
        )



    # -------------------------------
    # ADMIN ROLE
    # -------------------------------

    elif profile.role == "Admin":

        return render(
            request,
            "users/admin_dashboard.html",
            context
        )

    return redirect("login")
    # =====================================================
# STUDENT MANAGEMENT
# =====================================================

@login_required
@admin_or_teacher
def student_list(request):

    query = request.GET.get("q")

    students = User.objects.filter(
        profile__role="Student"
    ).select_related("profile")

    if query:

        students = students.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(profile__student_id__icontains=query)
        )

    return render(
        request,
        "users/student_list.html",
        {
            "students": students
        }
    )


@login_required
@admin_or_teacher
def add_student(request):

    if request.method == "POST":

        form = StudentForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )

            Profile.objects.create(
                user=user,
                role="Student",
                student_id=form.cleaned_data["student_id"]
)

            return redirect("student_list")

    else:

        form = StudentForm()

    return render(
        request,
        "users/add_student.html",
        {
            "form": form
        }
    )


@login_required
@admin_or_teacher
def edit_student(request, id):

    student = get_object_or_404(
        User,
        id=id,
        profile__role="Student"
    )

    if request.method == "POST":

        form = StudentForm(request.POST)

        if form.is_valid():

            student.username = form.cleaned_data["username"]
            student.email = form.cleaned_data["email"]

            student.profile.student_id = form.cleaned_data["student_id"]
            student.profile.save()

            if form.cleaned_data["password"]:
                student.set_password(
                    form.cleaned_data["password"]
                )

            student.save()

            return redirect("student_list")

    else:

        form = StudentForm(
            initial={
                "username": student.username,
                "email": student.email,
                "student_id": student.profile.student_id,
            }
        )

    return render(
        request,
        "users/add_student.html",
        {
            "form": form
        }
    )


@login_required
@admin_or_teacher
def delete_student(request, id):

    student = get_object_or_404(
        User,
        id=id,
        profile__role="Student"
    )

    student.delete()

    return redirect("student_list")

# =====================================================
# TEACHER MANAGEMENT
# =====================================================

@login_required
@admin_or_teacher
def teacher_list(request):

    query = request.GET.get("q")

    teachers = User.objects.filter(
        profile__role="Teacher"
    ).select_related("profile")

    if query:

        teachers = teachers.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )

    return render(
        request,
        "users/teacher_list.html",
        {
            "teachers": teachers
        }
    )


@login_required
@admin_or_teacher
def add_teacher(request):

    if request.method == "POST":

        form = TeacherForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )

            Profile.objects.create(
                user=user,
                role="Teacher"
            )

            return redirect("teacher_list")

    else:

        form = TeacherForm()

    return render(
        request,
        "users/add_teacher.html",
        {
            "form": form
        }
    )


@login_required
@admin_or_teacher
def edit_teacher(request, id):

    teacher = get_object_or_404(
        User,
        id=id,
        profile__role="Teacher"
    )

    if request.method == "POST":

        form = TeacherForm(request.POST)

        if form.is_valid():

            teacher.username = form.cleaned_data["username"]
            teacher.email = form.cleaned_data["email"]

            if form.cleaned_data["password"]:

                teacher.set_password(
                    form.cleaned_data["password"]
                )

            teacher.save()

            return redirect("teacher_list")

    else:

        form = TeacherForm(
            initial={
                "username": teacher.username,
                "email": teacher.email,
            }
        )

    return render(
        request,
        "users/add_teacher.html",
        {
            "form": form
        }
    )


@login_required
@admin_or_teacher
def delete_teacher(request, id):

    teacher = get_object_or_404(
        User,
        id=id,
        profile__role="Teacher"
    )

    teacher.delete()

    return redirect("teacher_list")
    # =====================================================
# PROFILE
# =====================================================

@login_required
def profile(request):

    profile = get_object_or_404(
        Profile,
        user=request.user
    )

    return render(
        request,
        "users/profile.html",
        {
            "profile": profile
        }
    )


@login_required
def edit_profile(request):

    user = request.user

    if request.method == "POST":

        user.username = request.POST.get("username")
        user.email = request.POST.get("email")

        password = request.POST.get("password")

        if password:
            user.set_password(password)

        user.save()

        return redirect("profile")

    return render(
        request,
        "users/edit_profile.html",
        {
            "user": user
        }
    )