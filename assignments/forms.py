from django import forms
from .models import Assignment


class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = "__all__"

        widgets = {
            "due_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
        }