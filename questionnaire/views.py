from typing import Union

from django.contrib import messages
from django.forms import ModelForm
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import QuizForm, QuestionForm, AnswerForm
from .models import Quiz, UserAnswer, Question, PassedPolls, AnswerQuestion


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
        messages.success(request, 'Вы успешно создали опрос!')
        return redirect('create_question')
    messages.error(request, 'Хм, что-то не то!')
    return redirect('create_poll')


@login_required
def create_question(request):
    if request.method == 'GET':
        context = {
            'form': QuestionForm()
        }
        return render(request, 'questionnaire/create_question.html', context)
    form = QuestionForm(request.POST)
    return process_form(request, form)


@login_required
def create_answer(request):
    if request.method == 'GET':
        context = {
            'form': AnswerForm()
        }
        return render(request, 'questionnaire/create_answer.html', context)
    form = AnswerForm(request.POST)
    return process_form(request, form, message_success='Вы создали ответ на вопрос!', func_redirect='create_answer')


@login_required
def my_poll(request):
    my_polls = Quiz.objects.filter(user=request.user).order_by('-created_at').prefetch_related()
    context = {
        'my_polls': my_polls,
        'UserAnswer': UserAnswer,
        'PassedPolls': PassedPolls,
    }
    return render(request, 'questionnaire/my_poll.html', context)


@login_required
def take_poll(request, poll_id):
    poll = get_object_or_404(Quiz, pk=poll_id)
    question = check_possibility_passing_poll(request, poll)
    if isinstance(question, HttpResponseNotFound):
        return question
    if request.method == 'GET':
        return get_standart_render(request, poll, question)
    number_question = request.POST.get('number_question')
    answers = request.POST.get('answers')

    all_question = poll.questions.all()
    # Обрабатываем кнопку "Назад", если нажата, возвращаем предыдущий вопрос
    if request.POST.get('redirect'):
        question = all_question.filter(pk=int(number_question)).first()
        return get_standart_render(request, poll, question)

    for i in request.POST.lists():
        answers = i[1] if i[0] == 'answers' else []  # Получаем ответ, который дал пользователь
    answer = UserAnswer(quiz=poll, question=get_object_or_404(Question, pk=int(number_question)),
                        answers=AnswerQuestion.objects.filter(pk=int(answers[0]))[0], user=request.user)
    answer.save()
    question = all_question.filter(pk=int(number_question) + 1).first()
    # Проверяем, есть ли вопрос, есл нет, то сообщаем об успешном прохождении опроса
    if not question:
        passed_quiz = PassedPolls(quiz=poll, passed_user=request.user)
        passed_quiz.save()
        messages.info(request, 'Вы успешно прошли опрос!')
        return redirect('index')
    return get_standart_render(request, poll, question)


def check_possibility_passing_poll(request, poll: Quiz) -> Union[Question, HttpResponseNotFound]:
    """
    Используется для проверки возможности пройти определённый опрос пользователем.
    request: WSGIRequest
    return: Question (вопрос на который пользователь будет отвечать)
            or HttpResponseNotFound (сообщение о невозможности пройти опрос).
    """
    check_poll_lifetime = _check_poll_lifetime(poll)
    if not isinstance(check_poll_lifetime, bool):
        return check_poll_lifetime
    if PassedPolls.objects.filter(quiz=poll, passed_user=request.user):
        return HttpResponseNotFound("Вы уже прошли этот опрос!")
    for question in poll.questions.all():
        if len(question.answers.all()) > 0:
            return question
    return HttpResponseNotFound("В этом опросе нет вопросов с ответами")


def get_standart_render(request, poll: Quiz, question: Question) -> HttpResponse:
    """ Возвращает стандартную страницу для ответа на вопрос в опросе. """
    context = {
        'poll': poll,
        'question': question,
    }
    return render(request, 'questionnaire/take_poll.html', context)


def process_form(request, form: ModelForm, message_success: str = 'Вы создали вопрос!',
                 message_error: str = 'Хм, что-то не то!',
                 func_redirect: str = 'create_question') -> HttpResponseRedirect:
    if form.is_valid():
        form.save()
        messages.info(request, message_success)
        return redirect(func_redirect)
    messages.error(request, message_error)
    return redirect(func_redirect)


def _check_poll_lifetime(poll: Quiz) -> Union[bool, HttpResponseNotFound]:
    """ Проверяем не кончился ли срок жизни опроса. """
    date_now = timezone.now()
    date_now.astimezone(timezone.utc).replace(tzinfo=None)
    if poll.lifetime <= date_now:
        return HttpResponseNotFound("Срок действия опроса истёк!")
    return True
