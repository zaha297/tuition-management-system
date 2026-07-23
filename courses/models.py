from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):

    course_name = models.CharField(max_length=100)

    teacher = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    limit_choices_to={"profile__role": "Teacher"},
    related_name="courses",
    null=True,
    blank=True,
)
    duration = models.CharField(max_length=50)

    fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.course_name


class Enrollment(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    enrollment_date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.student.username} - {self.course.course_name}"