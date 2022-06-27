from django.forms import ModelForm, DateTimeInput
from django.contrib.admin import widgets
from .models import *


class DateTimeInput(DateTimeInput):
    input_type = 'datetime-local'

class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description', 'topic', 'lifetime',)
        widgets = {
            'lifetime': DateTimeInput(),
        }
