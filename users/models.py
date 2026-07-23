from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    ROLE_CHOICES = (
        ("Admin", "Admin"),
        ("Teacher", "Teacher"),
        ("Student", "Student"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    student_id = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        if self.role == "Student" and not self.student_id:

            last_student = Profile.objects.filter(
                role="Student"
            ).order_by("-id").first()

            if last_student and last_student.student_id:

                last_number = int(last_student.student_id.replace("ST", ""))

                self.student_id = f"ST{last_number + 1:03d}"

            else:

                self.student_id = "ST001"

        super().save(*args, **kwargs)

    def __str__(self):

        if self.role == "Student":
            return f"{self.student_id} - {self.user.username}"

        return self.user.username