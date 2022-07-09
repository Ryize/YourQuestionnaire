from django import template
from collections import Counter

register = template.Library()


@register.filter(name='average')
def get_average(poll):
    user_quiz = poll.user_quiz.all()
    wrong_answer = [i.answers for i in user_quiz if not i.answers.correct]
    result_number = round((len(user_quiz) - len(wrong_answer)) / len(user_quiz) * 100, 1)
    result = f'<span style="color: green;">{result_number}%</span>'
    if result_number == 0:
        result = '<span style="color: red;">нет</span>'
    elif result_number < 26:
        result = f'<span style="color: red;">{result_number}%</span>'
    elif result_number < 50:
        result = f'<span style="color: Goldenrod;">{result_number}%</span>'
    elif result_number < 76:
        result = f'<span style="color: PaleGreen;">{result_number}%</span>'
    try:
        answer_with_most_errors = list(reversed(sorted(Counter(wrong_answer).items(), key=lambda x: x[1])))[0]
        return f'Правильных ответов: <strong>{result}</strong><br>Больше всего ошибок ({answer_with_most_errors[1]}): {answer_with_most_errors[0].question}'
    except:
        return f'Правильных ответов: <strong>{result}</strong>'

