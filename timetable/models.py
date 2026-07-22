from django.db import models
from courses.models import Course


class Timetable(models.Model):

    DAY_CHOICES = (
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    day = models.CharField(
        max_length=20,
        choices=DAY_CHOICES
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    room = models.CharField(
        max_length=50
    )

    class Meta:
        ordering = [
            "day",
            "start_time"
        ]

    def __str__(self):
        return f"{self.course.course_name} - {self.day}"