from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.http import HttpResponse, JsonResponse
from .serializers import *
from django.contrib import messages
from . forms import UserRegistrationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.utils.translation import gettext as _

# Create your views here.

def home(request):
    posts = Post.objects.count()
    groups = Group.objects.count()
    members = User.objects.count()
    return render(request, 'HuskersApp/home.html',
                  {'HuskersApp': home})

@login_required
def venue(request):
    venues = Venue.objects.filter(created_date__lte=timezone.now())
    venue = Venue.objects.all()
    return render(request, 'HuskersApp/venue.html',
                  {'HuskersApp': venue , 'venues': venues})

def feed(request):
    return render(request, 'HuskersApp/feed.html',
                  {'HuskersApp': feed})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'HuskersApp/register.html', {'form': form})

# def venue_detail(request):
#     return render(request, 'HuskersApp/venue_detail.html',
#                   {'HuskersApp': venue_detail},
#                   {'HuskersApp': home,
#                   'posts': posts,
#                   'groups': groups,
#                   'members': members})

"""
Manage Venues
"""

@login_required
def venue_list(request):
    """
    List All Venues available
    """
    #venues = Venue.objects.all()
    #serializer = VenueSerializer(venue, many=True)
    # TODO: List all new venues based on created_date
    venues = Venue.objects.filter(created_date__lte=timezone.now())
    # TODO: List all popular venues based on group count
    return render(request, 'HuskersApp/venue_list.html',
                    {'venues': venues})


@login_required
def venue_edit(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    if request.method == 'POST':
        form = VenueForm(request.POST, instance=venue)
        if form.is_valid():
            venue = form.save()
            venue.updated_date = timezone.now()
            venue.save()
            venues = Venue.objects.filter(created_date__lte=timezone.now())
            return render(request, 'HuskersApp/venue_list.html', {'venues': venues})

    else:
        form = VenueForm(instance=venue)
    return render(request, 'HuskersApp/venue_edit.html', {'form': form})


@login_required
def venue_new(request):
    """
    Add a new Venue
    """
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.created_date = timezone.now()
            venue.save()
            venues = Venue.objects.filter(created_date__lte=timezone.now())
            return render(request, 'HuskersApp/venue_list.html',
                            {'venues': venues})

    else:
        form = VenueForm()
    return render(request, 'HuskersApp/venue_new.html',
                    {'form': form})


@login_required
def venue_delete(request, pk):
    # TODO: Check Venue delete case
    venue = get_object_or_404(Venue, pk=pk)
    venue.delete()
    return redirect('HuskersApp/venue_list.html')


@login_required
def venue_detail(request, pk):
    # Based on venue Detail page in mockups
    venue = get_object_or_404(Venue, pk=pk)
    # Get all groups of which the venue is part of
    groups = Group.objects.filter(venue=pk)
    venue_weather_data = venue.venue_weather()
    city_id = venue_weather_data["id"]
    return render(request, 'HuskersApp/venue_detail.html',
                    {'venue': venue,
                     'groups': groups,
                     'cityId': city_id,
                     })


"""
Manage Groups
"""

@login_required
def group_list(request):
    """
    List All Groups
    """
    groups = Group.objects.all()
    # Get the current user
    currentUser = request.user
    # Get the groups of which the current user is a part
    currentUserGroups = User.objects.get(id=currentUser.id).group_set.all()
    return render(request, 'HuskersApp/group_list.html',
                    {'groups': groups,
                    'currentUserGroups': currentUserGroups})


@login_required
def group_detail(request, pk):
    # List details of a group
    group = get_object_or_404(Group, pk=pk)
    # Get the current user
    currentUser = request.user
    if currentUser in group.users.all():
        isGroupMember = True
    else:
        isGroupMember = False
    return render(request, 'HuskersApp/group_detail.html',
                    {'group': group,
                    'isGroupMember': isGroupMember})

@login_required
def group_new(request):
    """
    Add a new Group
    """
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_date = timezone.now()
            group.save()
            groups = Group.objects.filter(created_date__lte=timezone.now())
            return render(request, 'HuskersApp/group_list.html',
                            {'groups': groups})

    else:
        form = GroupForm()
    return render(request, 'HuskersApp/group_new.html',
                    {'form': form})


@login_required
def group_delete(request, pk):
    # TODO: Check Group delete case if user is admin of Group
    group = get_object_or_404(Group, pk=pk)
    group.delete()
    #TODO: Check which page to be routed
    return redirect('HuskersApp/group_list.html')


@login_required
def group_edit(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save(commit=False)
            group.updated_date = timezone.now()
            group.save()
            group = Group.objects.filter(created_date__lte=timezone.now())
            return render(request, 'HuskersApp/group_list.html',
                            {'group': group})

    else:
        form = GroupForm(instance=venue)
    return render(request, 'HuskersApp/group_edit.html',
                {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })

def update_user_group(request):
    userAction = request.GET.get('userAction', None)
    pk = request.GET.get('pk', None)
    currentUser = request.user
    group = get_object_or_404(Group, pk=pk)
    if userAction == 'leave':
        group.users.remove(currentUser)
        message = 'Successfully removed from group'
        userRemoved = True
        userAdded = False
    elif userAction == 'join':
        group.users.add(currentUser)
        message = 'Successfully added to group'
        userRemoved = False
        userAdded = True
    data = {
        'message': message,
        'userRemoved': userRemoved,
        'userAdded': userAdded
    }
    return JsonResponse(data)
