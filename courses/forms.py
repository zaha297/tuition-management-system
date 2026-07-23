from django import forms
from .models import Course, Enrollment


class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = [
            "course_name",
            "duration",
            "fee",
        ]


class EnrollmentForm(forms.ModelForm):

    class Meta:
        model = Enrollment
        fields = "__all__"