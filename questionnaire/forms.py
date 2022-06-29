from django.forms import ModelForm, DateTimeInput, Select
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


class QuestionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quiz'].empty_label = "Не выбрано!"

    class Meta:
        model = Question
        fields = ('question', 'quiz',)
        widgets = {
            'quiz': Select(attrs={'class': 'form-control', 'placeholder': 'Не выбрано!'}),
        }


class AnswerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].empty_label = "Не выбрано!"

    class Meta:
        model = AnswerQuestion
        fields = ('answer', 'question', 'correct', )
        widgets = {
            'question': Select(attrs={'class': 'form-control', 'placeholder': 'Не выбрано!'}),
        }
