from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.forms import model_to_dict
from . import models
from .forms import LoginForm, RegistrationForm, UserForm, ProfileForm, SettingsForm


def paginate(objects_list, request):
    paginator = Paginator(objects_list, 3)
    page = request.GET.get('page')
    objects_page = paginator.get_page(page)
    return objects_page


@login_required(login_url='login', redirect_field_name="continue")
def index(request):
    questions_list = models.Question.objects.new_questions()
    questions = paginate(questions_list, request)
    return render(request, 'index.html', {
        'questions': questions
    })


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect(request.META['HTTP_REFERER'])



def log_in(request):
    if request.method == "GET":
        login_form = LoginForm()

    elif request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Wrong username or password")

    return render(request, "login.html", context={'form': login_form})


def register(request):
    if request.method == 'GET':
        reg_form = RegistrationForm()
    elif request.method == 'POST':
        reg_form = RegistrationForm(data=request.POST, files=request.FILES)
        if reg_form.is_valid():
            user = reg_form.save()
            if user:
                # avatar = None ?
                auth.login(request, user)
                models.Profile.objects.create(user=user, avatar=reg_form.cleaned_data['avatar'])
                return redirect(reverse(viewname="index"))
            else:
                reg_form.add_error(None, "User saving error")
    context = {'form': reg_form}
    return render(request, "register.html", context=context)


def hot_view(request):
    questions_list = models.Question.objects.hot_questions()
    questions = paginate(questions_list, 3)
    return render(request, 'hot.html', {
        'objects': questions
    })


def question(request):
    answer = {'questions': models.QUESTIONS}
    return render(request, 'question.html', answer)


@login_required(login_url='login.html', redirect_field_name="continue")
def ask(request):
    return render(request, 'ask.html')


@login_required(login_url='login', redirect_field_name="continue")
def tag(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'tag.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


@login_required(redirect_field_name='/login')
def setting(request):
    if request.method == 'GET':
        dict_model_fields = model_to_dict(request.user)
        user_form = SettingsForm(initial=dict_model_fields)
    elif request.method == 'POST':
        user_form = SettingsForm(data=request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect(reverse("settings"))
    context = {'form': user_form }
    return render(request, "settings.html", context=context)