from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


# ==========================
# REGISTER FORM
# ==========================

class UserRegisterForm(UserCreationForm):

    ROLE_CHOICES = [
        ("Student", "Student"),
        ("Teacher", "Teacher"),
        ("Parent", "Parent"),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


# ==========================
# STUDENT FORM
# ==========================

class StudentForm(forms.Form):

    username = forms.CharField(max_length=150)

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False
    )

    student_id = forms.CharField(
        max_length=50,
        required=False
    )


# ==========================
# TEACHER FORM
# ==========================

class TeacherForm(forms.Form):

    username = forms.CharField(max_length=150)

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False
    )