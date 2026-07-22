from django.db import models
from django.contrib.auth.models import User
from courses.models import Course


class Fee(models.Model):
    PAYMENT_STATUS = (
        ("Paid", "Paid"),
        ("Pending", "Pending"),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE)

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="fee_records"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS)

    def __str__(self):
        return f"{self.student.username} - {self.course.course_name}"