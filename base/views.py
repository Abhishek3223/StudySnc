from django.shortcuts import render, redirect
from .models import Room, Topic, Message, User
from .form import Room_form, UserForm, myuserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from django.http import HttpResponse


def authPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        print(username, password)
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "Invalid username")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    context = {'page': page}
    return render(request, 'base/auth.html', context)


def logoutPage(request):

    logout(request)

    return redirect('home')


def registerUser(request):
    page = 'register'
    if request.user.is_authenticated:
        return redirect('home')

    form = myuserCreationForm()
    if request.method == "POST":
        form = myuserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('home')

        else:
            messages.error(request, "Error occurred !!")
    context = {'page': page, 'form': form}

    return render(request, 'base/auth.html', context)


@login_required(login_url='authPage')
def home(request):
    # return HttpResponse("hey home page")
    # print(Rooms)
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    Rooms = Room.objects.filter(
        Q(topic__name__icontains=q)
        | Q(name__icontains=q)
        | Q(discription__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = Rooms.count()

    recent_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': Rooms, 'topics': topics,
               'room_count': room_count, 'recent_messages': recent_messages}
    # print(rooms[0].host.id)
    return render(request, "base/home.html", context)


# ---------------------------------------------------------
@login_required(login_url='authPage')
def room(request, pk):
    # return HttpResponse("hey room page")

    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == "POST":

        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, "base/room.html", context)

# ----------------------------------------------


def userProfile(request, pk):
    user = User.objects.get(email=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


# --------------------------------------------------------
@login_required(login_url='authPage')
def create_room(request):
    # return HttpResponse("hey home page")
    # print(Rooms)
    form = Room_form()
    topic = Topic.objects.all()
    if request.method == "POST":
        form = Room_form(request.POST)

        topic_name = request.POST.get('topic')
        print(topic_name)
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            discription=request.POST.get('discription')
        )
        return redirect('home')
    context = {'form': form, "topics": topic}
    return render(request, "base/room_form.html", context)


@login_required(login_url='authPage')
def Update_room(request, pk):
    # return HttpResponse("hey home page")
    # print(Rooms)
    room = Room.objects.get(id=pk)
    form = Room_form(instance=room)
    topic = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('you are not allowed !!')

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.discription = request.POST.get('discription')
        room.save()
        # form = Room_form(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')

    context = {'form': form, "topics": topic}
    return render(request, "base/room_form.html", context)


@login_required(login_url='authPage')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('you are not allowed !!')

    if request.method == "POST":
        room.delete()
        return redirect('home')

    context = {'obj': room}

    return render(request, "base/delete.html")


@login_required(login_url='authPage')
def delete_msg(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('you are not allowed !!')

    if request.method == "POST":
        message.delete()
        return redirect('home')

    context = {'obj': message}

    return render(request, "base/delete.html", context)


@login_required(login_url='authPage')
def update_user(request):
    user = request.user
    form = UserForm(instance=request.user)
    # user = User.objects.get(id=pk)
    # form = User_form(instance=user)
    if request.method == "POST":
        print('ok1')
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_Profile', pk=user)
    context = {'form': form}
    return render(request, "base/update_user.html", context)


def topic_page(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)[0:5]
    return render(request, "base/topics.html", {'topics': topics})


def activity_page(request):
    recent_messages = Message.objects.all()
    return render(request, "base/activity.html", {"messages": recent_messages})
