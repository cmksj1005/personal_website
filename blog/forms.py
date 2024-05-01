from django import forms

from .models import Feedback

class FeedbackForm(forms.ModelForm):
  class Meta:
    model = Feedback
    exclude = ["Project"]
    labels = {
      "user_name": "Your Name",
      "user_email": "Your Email",
      "text": "Your Feedback"
    }