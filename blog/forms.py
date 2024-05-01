from django import forms

from .models import Feedback

class FeedbackForm(forms.ModelForm):
  class Meta:
    model = Feedback
    exclude = ["project", "edit"]
    labels = {
      "user_name": "Name",
      "user_password": "Password",
      "text": "Feedback"
    }