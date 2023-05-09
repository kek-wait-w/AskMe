from django.shortcuts import render
from . import models


def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'index.html', context)


def question(request):
    answer = {'questions': models.QUESTIONS}
    return render(request, 'question.html', answer)


def ask(request):
    return render(request, 'ask.html')


def register(request):
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')


def tag(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'tag.html', context)


