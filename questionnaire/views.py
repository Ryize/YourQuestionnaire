from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import QuizForm, QuestionForm, AnswerForm


def index(request):
    return render(request, 'questionnaire/index.html')


@login_required
def create_poll(request):
    if request.method == 'GET':
        context = {
            'form': QuizForm()
        }
        return render(request, 'questionnaire/create_poll.html', context)
    form = QuizForm(request.POST)
    if form.is_valid():
        form_with_user = form.save(commit=False)
        form_with_user.user = request.user
        form_with_user.save()
        return redirect('create_question')
    return redirect('create_poll')


@login_required
def create_question(request):
    if request.method == 'GET':
        context = {
            'form': QuestionForm()
        }
        return render(request, 'questionnaire/create_question.html', context)
    form = QuestionForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('create_poll')
    return redirect('create_poll')


@login_required
def create_answer(request):
    if request.method == 'GET':
        context = {
            'form': AnswerForm()
        }
        return render(request, 'questionnaire/create_answer.html', context)
    form = AnswerForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('create_answer')
    return redirect('create_answer')