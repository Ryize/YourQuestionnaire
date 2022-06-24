from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'questionnaire/index.html')


@login_required
def create_poll(request):
    pass