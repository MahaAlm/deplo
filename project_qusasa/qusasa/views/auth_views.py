from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from ..forms import CustomUserCreationForm  # Import at the top
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from ..models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from ..utils import searchByQuery, extractIdFromUrl, analyse_channels, video_analysis, analyze_playlist, analyze_channel, download_audio_from_youtube, transcribe_youtube_video, summarize_youtube_video, create_word_document, topic_analysis, get_realted_videos
from ..youtube_api import get_youtube_client
from django.core.exceptions import ValidationError
import re
import os
from django.conf import settings
from ..models import Inquiry
from ..models import TopicAnalysisHistory
import openai
import pandas as pd
from ..models import Inquiry
from django.shortcuts import render, get_object_or_404

def custom_admin(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'admin/custom_admin.html', context)


def email_verified_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_verified:
            return function(request, *args, **kwargs)
        else:
            return redirect('confirm_email')
    return wrap


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'qusasa.backends.EmailBackend'
            
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'qusasa/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_verified:
                return redirect('base')
            else:
                # Redirect to a page where they need to input the confirmation code
                return redirect('confirm_email')  # Change to the name/url of your confirmation code input page
        else:
            return render(request, 'qusasa/login.html', {'error': 'Invalid email or password.'})
    return render(request, 'qusasa/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@staff_member_required
@email_verified_required
def admin_only_pages(request):
    return render(request,'login.html')

def YouTubeFeat(request):
    return render(request,'qusasa/YouTubeFeat.html')
def InstagramFeat(request):
    return render(request,'qusasa/InstagramFeat.html')
def wFeature(request):
    return render(request,'qusasa/wFeature.html')


@login_required
def confirm_email(request):
    if request.method == 'POST':
        input_code = request.POST['confirmation_code']
        user = request.user
        if user.email_confirmation_code == input_code:
            user.is_verified = True
            user.email_confirmation_code = None  # Clear the confirmation code
            user.save()
            return redirect('base')
        else:
            # Handle incorrect code, maybe show an error message on the confirmation page
            return render(request, 'qusasa/confirm_email.html', {'error': 'Invalid confirmation code.'})
    else:
        # Display the page where they input the confirmation code
        return render(request, 'qusasa/confirm_email.html')
 
@staff_member_required
def inquiries_view(request):
    context={
        'posts':Inquiry.objects.all()
    }
    return render(request, 'admin/inquiries.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from ..forms import InquiryForm
from ..models import Inquiry
from django.utils import timezone,dateformat

def display_inquiry(request, history_id):
    inquiry = get_object_or_404(Inquiry, pk=history_id)
    updates = inquiry.InqContent.split('\n\n\t\n\n')
    co=updates.count

    if request.method == 'POST':
        form = InquiryForm(request.POST, instance=inquiry)
        if form.is_valid():
            updated_inquiry = form.save(commit=False)
            updated_inquiry.status = 'RESOLVED'  # Set status to 'RESOLVED'
            updated_inquiry.date_resolved = timezone.now()  # Update the resolved date to now
            updated_inquiry.save()  # Save the changes to the database
            # Redirect to a new URL or render a template with a success message
    else:
        form = InquiryForm(instance=inquiry)
    
    return render(request, 'admin/display_inquiry.html', {'count':co,'updates':updates,'form': form, 'history': inquiry})

def user_inquiries_view(request):
    user_inquiries = Inquiry.objects.filter(author=request.user)
    
    context = {
        'posts': user_inquiries
    }
    return render(request, 'qusasa/user_inquiries.html', context)

def add_inquiry(request):
    
    if request.method == "POST":
        title = request.POST.get('title', '') 
        inq_content = request.POST.get('inq_content', '')
        
        status = 'WAITING'
        # Create the new Inquiry instance
        new_inquiry = Inquiry(
            title=title,
            InqContent=inq_content,
            RepContent='', 
            status=status,
            date_posted=timezone.now(),
            author=request.user
        )
        # Save the new inquiry
        new_inquiry.save()
        
        # Redirect to a new URL after saving:
        return redirect('user_inquiries')  # Redirect to an appropriate view after saving

    return render(request, 'qusasa/add_inquiry.html')

def update_inquiry(request, inquiry_id):
    # Get the Inquiry instance you want to update
    inquiry = get_object_or_404(Inquiry, pk=inquiry_id)
    updates = inquiry.InqContent.split('\n\n\t\n\n')


    if request.method == "POST":
        new_content = request.POST.get('inq_content', '')
        if new_content!='':
            inquiry.InqContent += "\n\n\t\n\n, "+new_content+"\n"+str(dateformat.format(timezone.localtime(timezone.now()),'Y-m-d ',))
            inquiry.status='WAITING'


        # Save the updated inquiry
        inquiry.save()
        
        # Redirect to a new URL after saving:
        
        return redirect('user_inquiries')  # Adjust the redirect as needed to go back to the listing or detail view

    else:
        # Assuming you are passing the inquiry instance to the template to pre-fill the form fields with existing data
        return render(request, 'qusasa/update_inquiry.html', {'updates': updates,'inquiry': inquiry})
    

def user_display_inquiry(request, history_id):
    inquiry = get_object_or_404(Inquiry, pk=history_id)
    updates = inquiry.InqContent.split('\n\n\t\n\n')
    form = InquiryForm(instance=inquiry)
    
    return render(request, 'qusasa/user_display_inquiry.html', {'updates': updates,'form': form, 'history': inquiry})
