from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from . import models

from .forms import LoginForm


def paginate(objects_list, request):
    paginator = Paginator(objects_list, 30)
    page = request.GET.get('page')
    objects_page = paginator.get_page(page)
    return objects_page


@login_required(login_url='login', redirect_field_name="continue")
def index(request):
    questions_list = models.Question.objects.new_questions()
    questions = paginate(questions_list, request)
    return render(request, 'index.html', {
        'objects': questions
    })


def log_in(request):
    if request.method == 'GET':
        login_form = LoginForm()
    elif request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                login(request, user)
                return redirect(reverse('index'))
            login_form.add_error(field=None, error="Wrong login or password ")

    return render(request, "login.html", context={'form': login_form})


def signup(request):
    if request.method == 'GET':
        user_form = RegistrationForm()
    elif request.method == 'POST':
        user_form = RegistrationForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="User saving error!")
    return render(request, "register.html", {'form': user_form})


def question(request):
    answer = {'questions': models.QUESTIONS}
    return render(request, 'question.html', answer)


def ask(request):
    return render(request, 'ask.html')


def register(request):
    return render(request, 'register.html')


def tag(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'tag.html', context)
