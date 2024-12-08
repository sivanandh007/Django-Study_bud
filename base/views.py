from django.shortcuts import render , redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from .models import Room , topic
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

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q)
                                )
    topics = topic.objects.all()
    room_count = rooms.count()
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count}
    return render(request, 'base/home.html',context)
def room(request , ids):
    room = Room.objects.get(id=ids)
    context = {'room':room}
    return render(request,'base/room.html',context)


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

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have logged in successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'base/login_register.html')

    # For GET requests or failed POST
    return render(request, 'base/login_register.html')
