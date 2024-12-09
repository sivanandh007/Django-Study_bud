from django.shortcuts import render , redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .models import Room , topic , Message
from .forms import RoomForm

# Create your views here.

# rooms =[
#     {'id':1, 'name':'lets learn python'},
#     {'id':2, 'name':'Develop with me'},
#     {'id':3, 'name':'Frontend Developer'},       
# ]

def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
         messages.error(request,'An error occured during registration')

    return render(request,'base/login_register.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q)
                                )
    topics = topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.all().filter(Q(room__topic__name__icontains=q))
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html',context)
def room(request , ids):
    room = Room.objects.get(id=ids)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',ids=room.id)

    context = {'room':room, 'room_messages': room_messages, 'participants': participants}
    return render(request,'base/room.html',context)

def userProfile(request):
    context = {}
    return render(request,'base/profile.html',context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context= {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)


    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':room})


def loginPage(request):
    page = 'login'


    if request.user.is_authenticated:
        return redirect('home')


    storage = get_messages(request)
    list(storage)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Both username and password are required.')
            return render(request, 'base/login_register.html')

        # Debugging: Log input
        print(f"Username: {username}, Password: {password}")
        username = username.lower()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have logged in successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'base/login_register.html')

    context = {'page':page}
    # For GET requests or failed POST
    return render(request, 'base/login_register.html',context)

@login_required(login_url='login')
def deleteMessage(request,pk):
    messgae = Message.objects.get(id=pk)


    if request.user != messgae.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        messgae.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj':messgae})
