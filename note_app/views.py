from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from note_app.models import Notes


def home(request):
    return render(request, 'note_app/login_signup.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['uname']
        password = request.POST['pass']
        cnf_password = request.POST['cnf_pass']
        try:
            user = User.objects.create_user(username, email, password)
            user.name = name
            user.save()
        except Exception as e:
            messages.error(request, 'Username already exist...')
            print(e)

    return render(request, "note_app/login_signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['u_name']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            name = user.get_username()
            return redirect('user_home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect("home")


def sign_out(request):
    logout(request)
    return redirect("home")


@login_required(login_url='home')
def new_note(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        user = request.user
        id = request.POST['id']
        if not id:
            Notes(title=title, user=user, content=content).save()
            messages.success(request, f'New note created!')
            return redirect("all_notes")
        else:
            Notes.objects.filter(id=id).update(title=title, user=user, content=content)
            return redirect("all_notes")
    return render(request, 'note_app/new_note.html', {'note_count': Notes.objects.filter(user=request.user).count(),
                                                      'btn': 'Add'})


@login_required(login_url='home')
def all_notes(request):
    user_all_notes = Notes.objects.filter(user=request.user).reverse()
    return render(request, "note_app/all_notes.html", {'all_notes': user_all_notes,
                                                       'note_count': Notes.objects.filter(user=request.user).count(),
                                                       'func': 'Your All Notes.'})


@login_required(login_url='home')
def user_home(request):
    return render(request, 'note_app/user_home.html', {'note_count': Notes.objects.filter(user=request.user).count()})


@login_required(login_url='home')
def search(request):
    if 'title' in request.POST:
        title = request.POST['title']
        notes = Notes.objects.filter(user=request.user, title__icontains=title)
        return render(request, "note_app/all_notes.html",
                      {'all_notes': notes, 'note_count': Notes.objects.filter(user=request.user).count(),
                       'func': 'Search Result....'})


@login_required(login_url='home')
def update(request, id):
    note = Notes.objects.get(id=id)
    return render(request, 'note_app/new_note.html', {'note': note,
                                                      'note_count': Notes.objects.filter(user=request.user).count(),
                                                      'btn': 'Update'})


@login_required(login_url='home')
def delete(request, id):
    Notes.objects.filter(user=request.user).get(id=id).delete()
    return redirect("all_notes")
