from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
from myapp.models import Problem

MODER_GROUP_NAME = 'moders'


def index(request):
    # если мы залогинены
    if request.user.is_authenticated:
        admin = check_moder(request)
        if admin:
            user = request.user.username
            problems = Problem.objects.filter(solved=False, curator=None)
            solvedproblems = Problem.objects.filter(solved=True)
            myproblems = Problem.objects.filter(solved=False, curator=request.user, progress=True)
            return render(request, "admin.html",
                          {'username': user, 'problems': problems, 'myproblems': myproblems, 'solvedproblems': solvedproblems})
        user = request.user.username
        problems = Problem.objects.filter(solved=False)
        myproblems = problems.filter(author=request.user)
        solvedproblems = Problem.objects.filter(solved=True)
        return render(request, "indexAuth.html", {'username': user, 'problems': problems, 'myproblems': myproblems,
                                                  'solvedproblems': solvedproblems})
    else:
        if request.method == 'POST':
            if request.POST['button'] == 'Войти или Зарегестрироваться':
                user = request.POST['username']
            return redirect('/login?user={}'.format(user))
        problems = Problem.objects.filter(solved=False)
        solvedproblems = Problem.objects.filter(solved=True)
        return render(request, "index.html", {'problems': problems, 'solvedproblems': solvedproblems})


def login_page(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        userlogin = request.GET['user']
        if User.objects.filter(username=userlogin).exists():
            return render(request, 'login.html', {'username': userlogin})
        else:
            return redirect('/register?user={}'.format(userlogin))
    if request.method == 'POST':
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')

        if username == '' or password == '':
            return HttpResponse("Заполните все поля")

        # проверяем правильность логина и пароля
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Неправильный логин или пароль!')
            return redirect('/login?user=' + username)


def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        userlogin = request.GET['user']
        return render(request, 'register.html', {'username': userlogin})
    if request.method == 'POST':
        username = request.POST.get('login', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        if username == '' or password1 == '' or password2 == '':
            messages.error(request, 'Не все поля заполнены')
            return redirect('/register?user' + username)
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ник уже занят')
            return redirect('/register?user=' + username)
        if len(username) < 3:
            messages.error(request, 'Слишком короткий ник')
            return redirect('/register?user=' + username)
        if len(username) > 20:
            messages.error(request, 'Слишком длинный ник')
            return redirect('/register?user=' + username)
        if len(password1) < 6:
            messages.error(request, 'Слишком короткий пароль')
            return redirect('/register?user=' + username)
        if len(password1) > 50:
            messages.error(request, 'Слишком длинный пароль')
            return redirect('/register?user=' + username)
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
            return redirect('/register?user=' + username)
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            login(request, user)
            return redirect('/')


def logout_page(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/')


def addproblem(request):
    if not (request.user.is_authenticated):
        return redirect('/')
    if request.method == 'POST':

        if request.POST.get('text', '') == "":
            messages.error(request, 'Заполните описание')
            return redirect('/addproblem')
        if request.POST.get('title', '') == "":
            messages.error(request, 'Введите название')
            return redirect('/addproblem')

        problem = Problem()
        problem.text = request.POST['text']
        problem.author = request.user
        problem.home = request.POST['home']
        problem.title = request.POST['title']
        problem.save()
        return redirect('/')

    return render(request, "AddProblem.html", {'username': request.user.username})


def like(request):
    id = request.GET['id']
    problem = Problem.objects.get(pk=id)
    problem.likes.add(request.user)
    return redirect('/')


def check_moder(r):
    return r.user.groups.filter(name=MODER_GROUP_NAME).exists()


def check(request):
    fallback = request.GET.get('fallback', '/')
    if check_moder(request):
        idd = request.GET.get('id')
        a_type = request.GET.get('type')
        if idd and a_type:
            problem = Problem.objects.get(pk=idd)
            if a_type == 'start':
                problem.progress = True
                problem.curator = request.user
            if a_type == 'finish':
                problem.progress = False
                problem.solved = True
            problem.save()
    return redirect(fallback)


