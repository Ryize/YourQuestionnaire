from django.contrib.auth.models import User
from django.db import models


class Quiz(models.Model):
    title = models.CharField(max_length=64, verbose_name='Название')
    description = models.CharField(max_length=256, verbose_name='Описание')
    topic = models.CharField(max_length=64, verbose_name='Тема')
    lifetime = models.DateTimeField(verbose_name='Действует до')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return f'{self.title}, {self.topic}'

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    question = models.CharField(max_length=64, verbose_name='Вопрос')
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, verbose_name='Опрос', related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return f'{self.question}'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class AnswerQuestion(models.Model):
    answer = models.CharField(max_length=64, verbose_name='Ответ')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='Вопрос', related_name='answers')
    correct = models.BooleanField(default=False, verbose_name='Это правильный ответ?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
