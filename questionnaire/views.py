from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import QuizForm, QuestionForm, AnswerForm
from .models import Quiz, UserAnswer, Question


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
        return redirect('create_question')
    return redirect('create_question')


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


@login_required
def my_poll(request):
    my_polls = Quiz.objects.filter(user=request.user).order_by('-created_at').prefetch_related()
    context = {
        'my_polls': my_polls,
    }
    return render(request, 'questionnaire/my_poll.html', context)


@login_required
def take_poll(request, poll_id):
    poll = get_object_or_404(Quiz, pk=poll_id)
    for question in poll.questions.all():
        if len(question.answers.all()) > 0:
            break
    else:
        return HttpResponseNotFound("В этом опросе нет вопросов с ответами")

    if request.method == 'POST':
        number_question = request.POST.get('number_question')
        answers = request.POST.get('answers')
        for i in request.POST.lists():
            answers = i[1] if i[0] == 'answers' else []
        for question in poll.questions.all():
            correct_answers = question.answers.filter(correct=True)
            if correct_answers:
                for i in correct_answers:
                    if str(i.pk) in answers:
                        answer = UserAnswer(quiz=poll, question=get_object_or_404(Question, pk=int(number_question)),
                                            answers=i, user=request.user)
                        answer.save()
                    else:
                        pass
        all_question = poll.questions.all()
        question = all_question.filter(pk=int(number_question)+1).first()
        if not question:
            return redirect('index')
    context = {
        'poll': poll,
        'question': question,
    }
    return render(request, 'questionnaire/take_poll.html', context)
