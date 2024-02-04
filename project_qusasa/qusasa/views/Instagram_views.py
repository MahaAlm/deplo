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
from ..utils import parse_datetime, searchByQuery, extractIdFromUrl, analyse_channels, video_analysis, analyze_playlist, analyze_channel, download_audio_from_youtube, transcribe_youtube_video, summarize_youtube_video, create_word_document, topic_analysis, get_realted_videos
from ..youtube_api import get_youtube_client
from django.core.exceptions import ValidationError
import re
import os
from django.conf import settings
import openai
import pandas as pd
from .auth_views import *
from django.http import FileResponse, Http404
import os
import json
from django.shortcuts import render, get_object_or_404
from .doc_views import *
from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
import zipfile
import io

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#Post_Analysis
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

def posts_analysis_detail(request, history_id):
    history = get_object_or_404(PostAnalysisHistory, pk=history_id, user=request.user)
    return render(request, 'instafeatures_pages/playlist_analysis/posts_analysis_detail.html', {'history': history})

def posts_analysis_details(request):
    # You can add code here to fetch and process inquiries
    return render(request, 'instafeatures_pages/posts_analysis/posts_analysis_details.html')


from ..forms import PostAnalysisInputForm
from ..models import  PostAnalysisHistory
class PostAnalysisWizard(SessionWizardView):
    form_list = [PostAnalysisInputForm]
    template_name = 'instafeatures_pages/posts_analysis/posts_analysis_forms.html'  
    
    # def get_form_initial(self, step):
    #     initial = super().get_form_initial(step)
    #     history_id = self.kwargs.get('history_id')

    #     if history_id and step == '0':  # Assuming '0' is the step of PlaylistAnalysisInputForm
    #         history = get_object_or_404(PostAnalysisHistory, id=history_id, user=self.request.user)
    #         initial.update({
    #             'post_url': history.playlist_url,
    #             # Add other fields as necessary
    #         })
    #     return initial
    
    def done(self, form_list, **kwargs):
        # Process the cleaned data
        cleaned_data = self.get_all_cleaned_data()
        post_url = cleaned_data.get('post_url')
        
        # history_id = self.kwargs.get('history_id')
        # if history_id:
        #     # Update the existing history record
        #     history = get_object_or_404(PostAnalysisHistory, id=history_id, user=self.request.user)
        #     history.post_url = cleaned_data.get('post_url')
        #     # Update other fields as necessary
        #     history.save()
        # else:
        #     PostAnalysisHistory.objects.create(
        #     user=self.request.user,
        #     post_url=cleaned_data.get('post_url'),
        #     )
        
        
        return HttpResponseRedirect(reverse('post_analysis_output'))  # Use the name of the URL pattern

import math
from datetime import datetime

def posts_analysis_output_view(request):
    
   
    return render(request, 'instafeatures_pages/posts_analysis/posts_analysis_output.html')

def posts_dataset_zipped_output(request):
    # Handle the output display here
    # Retrieve the CSV data from the session
    playlist_info_csv = request.session.get('playlist_info_csv', '')
    all_videos_info_csv = request.session.get('all_videos_info_csv', '')
    # Create a zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr('playlist_info_csv.csv', playlist_info_csv)
        zip_file.writestr('all_videos_info_csv.csv', all_videos_info_csv)

    # Set up the HttpResponse
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="playlist_analysis_datasets.zip"'

    return response

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#Topic Trend Analysis
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

def topictrend_analysis_details(request):
    # You can add code here to fetch and process inquiries
    return render(request, 'instafeatures_pages/topictrend_analysis/topictrend_analysis_details.html')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#Engagement History
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

def engagement_history_details(request):
    # You can add code here to fetch and process inquiries
    return render(request, 'instafeatures_pages/engagement_history/engagement_history_details.html')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#People Analysis
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

def people_analytics_details(request):
    # You can add code here to fetch and process inquiries
    return render(request, 'instafeatures_pages/people_analytics/people_analytics_details.html')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#Comparative Study
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

def comparative_study_details(request):
    # You can add code here to fetch and process inquiries
    return render(request, 'instafeatures_pages/comparative_study/comparative_study_details.html')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#Reporting
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

def instagram_reporting_details(request):
    # You can add code here to fetch and process inquiries
    return render(request, 'instafeatures_pages/instagram_reporting/instagram_reporting_details.html')
