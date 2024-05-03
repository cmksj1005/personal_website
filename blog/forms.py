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
    widgets = {
      'user_password': forms.PasswordInput(),  # This tells Django to use the password input widget
    }