from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User, Report, Image
from .forms import RoomForm, UserForm, MyUserCreationForm, ReportForm, ImageForm
from django.template import *

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page,
                'is_home': request.path == '/',}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, form.errors)
            
    context = {'form': form,
                'is_home': request.path == '/',}

    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    oo = request.GET.get('order_option') if request.GET.get('order_option') != None else 'created'
    
    od = request.GET.get('order_direction') if request.GET.get('order_direction') != None else 'descending'
    direction_symbol = '-' if (od == 'descending') else ''


    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    ).order_by(str(direction_symbol+oo))
    # ).order_by(oo)
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms,
               'topics': topics,
               'room_count': room_count,
               'room_messages': room_messages,
               'is_home': request.path == '/',
            }
    
    return render(request, 'base/home.html', context)

def likedRooms(request):
    user = request.user
    liked_rooms = Room.objects.filter(likes=user)
    room_count = liked_rooms.count()

    context = {'liked_rooms': liked_rooms,
               'room_count': room_count,
                'is_home': request.path == '/',}
    return render(request, 'base/liked_rooms.html', context)



def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        message.room.message_count = Message.objects.filter(room=room).count()
        message.room.save()
        
        room.participants.add(request.user)
        
        return redirect('room', pk=room.id)

    context = {'room': room,
               'room_messages': room_messages,
               'participants': participants,
                'is_home': request.path == '/',}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_count = Room.objects.all().count()
    
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages,
               'topics': topics,
               'room_count': room_count,
                'is_home': request.path == '/',}
    
    return render(request, 'base/profile.html', context)

# def linebreak_description(description):
#     linebreak_description = ""
#     counter = 0
#     for i, letter in enumerate(description):
#         if letter == '\n':
#             counter = 0
#         if counter % 80 == 0:
#             linebreak_description += '\n'
#             counter = 0
#         linebreak_description += letter
#         counter += 1
#     return linebreak_description

# this is just because at the beginning too a `\n` character gets added

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    imageform = ImageForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        
        form = RoomForm(request.POST)
        files = request.FILES.getlist("image")
        
        if form.is_valid():
            f = form.save(commit=False)
            f.host = request.user
            topic_name = request.POST.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)

            if topic != None:
                topic.post_count += 1        

            elif created:
                topic.creator=request.user
                topic.name = topic_name
                topic.description = ""
            
            
            f.topic = topic
            f.name = request.POST.get('name')
            f.description = request.POST.get('description')
            f.save()
            if files:
                for i in files:
                    Image.objects.create(room=f, image=i)
            messages.success(request, "New Post created!")
        else:
            messages.error(request, form.errors)
        return redirect('home')
    context = {'form':form,
               'topics':topics,
               'imageform':imageform,
                'is_home': request.path == '/',}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    current_topic = room.topic
    form = RoomForm(instance=room)
    imageform = ImageForm()
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        files = request.FILES.getlist("image")
        
        if form.is_valid():
            f = form.save(commit=False)
            f.host = request.user
            topic_name = request.POST.get('topic')
            topic, create = Topic.objects.get_or_create(name=topic_name)
            f.topic = topic
            f.name = request.POST.get('name')
            f.description = request.POST.get('description')
            f.save()
            if files:
                for i in files:
                    Image.objects.create(room=f, image=i)
            messages.success(request, "Post Edited!")
            return redirect('home')
        else:
            messages.error(request, form.errors)
            return redirect('home')

    context = {'form':form,
               'current_topic': current_topic,
               'topics':topics,
               'imageform':imageform,
                'is_home': request.path == '/',}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room,
               'is_home': request.path == '/',}
    return render(request, 'base/delete.html', context=context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        message.room.message_count -= 1
        return redirect('home')
    
    context = {'obj': message,
            'is_home': request.path == '/',}
    return render(request, 'base/delete.html', context=context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    current_avatar_url = user.avatar.url[8:]
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            # user.avatar.url = request.POST.get('avatar').url
            return redirect('user-profile', pk=user.id)
        else:
            messages.error(request, form.errors)
    context = {'form': form,
               'current_avatar_url': current_avatar_url,
                'is_home': request.path == '/',}
    return render(request, 'base/update-user.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    room_count = Room.objects.all().count()
    context = {'topics': topics,
               'room_count': room_count,
               'is_home': request.path == '/'}
    return render(request, 'base/topics.html', context)


def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages, 'is_home': request.path == '/'}
    return render(request, 'base/activity.html', context)

@login_required(login_url='login')
def likeRoom(request, pk):
    user = request.user
    room_obj = Room.objects.get(id=pk)
    
    if request.method == 'POST':
        if user in room_obj.likes.all():
            room_obj.likes.remove(user)
            room_obj.like_count = room_obj.likes.count()
            room_obj.save()

        else:
            room_obj.likes.add(user)
            room_obj.like_count = room_obj.likes.count()
            room_obj.save()
            
        return redirect('room', pk=pk)

    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def reportRoom(request, pk):
    form = ReportForm()
    if request.method == 'POST':
        Report.objects.create(
            user = request.user,
            room = Room.objects.get(id=pk),
            reason = request.POST.get('reason'),
        )
        return redirect('home')
    
    room = Room.objects.get(id=pk)
    context = {'form': form, 'room': room, 'is_home': request.path == '/'}
    return render(request, 'base/report.html', context)
    
@login_required(login_url='login')
def reportManagementPage(request):
    report_requests = Report.objects.all()
    context = {'report_requests': report_requests, 'is_home': request.path == '/'}
    return render(request, 'base/report_management.html', context)


@login_required(login_url='login')
def censorReportedRoom(request, pk):
    report_request = Report.objects.get(id=pk)

    if request.method == 'POST':
        if request.POST.get('censor_result') == 'Pass Report Request (Delete Post)':
            report_request.room.delete()
            Report.objects.filter(id=report_request.id).delete()

        elif request.POST.get('censor_result') == 'Deny Report Request (Delete Request)':
            report_request.delete()
            
        return redirect('report-management')
    context = {'report_request': report_request, 'is_home': request.path == '/'}
    return render(request, 'base/censorReportedRoom.html', context)