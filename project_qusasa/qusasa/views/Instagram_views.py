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
from ..utilsInstagram import postAnalysis
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
        post_id = cleaned_data.get('post_url')
        
        PostDf, commentDataset ,comment_sentiments, sentiments, num_pics = postAnalysis(post_id)
        history_id = self.kwargs.get('history_id')
        if history_id:
            # Update the existing history record
            history = get_object_or_404(PostAnalysisHistory, id=history_id, user=self.request.user)
            history.post_url = cleaned_data.get('post_url')
            # Update other fields as necessary
            history.save()
        else:
            PostAnalysisHistory.objects.create(
            user=self.request.user,
            post_url=cleaned_data.get('post_url'),
            )
        
        commentDataset_csv = pd.DataFrame(commentDataset).to_csv(index=False)
        Post_csv = PostDf.to_csv(index=False)
        
        self.request.session['num_pics'] = num_pics
        self.request.session['commentDataset_csv'] = commentDataset_csv
        self.request.session['Post_csv'] = Post_csv
        self.request.session['publishedAt'] = PostDf['publishedAt'].iloc[0]
        self.request.session['owner'] = PostDf['owner'].iloc[0]
        self.request.session['thumbnial_url'] = PostDf['thumbnial_url'].iloc[0]
        self.request.session['icon_url'] = PostDf['icon_url'].iloc[0]
        self.request.session['top_keywords'] = PostDf['top_keywords'].iloc[0]
        self.request.session['MediaCount'] = int(PostDf['MediaCount'].iloc[0])
        self.request.session['followerCount'] = int(PostDf['followerCount'].iloc[0])
        self.request.session['followingCount'] = int(PostDf['followingCount'].iloc[0])
        self.request.session['LikeCount'] = int(PostDf['LikeCount'].iloc[0])
        self.request.session['CommentCount'] = int(PostDf['CommentCount'].iloc[0])

        self.request.session['caption'] = str(PostDf['caption'].iloc[0])
        self.request.session['CommentDate'] = pd.DataFrame(commentDataset)['CommentDate'].tolist()
        self.request.session['CommentLikes'] = pd.DataFrame(commentDataset)['CommentLikes'].tolist()
        
        self.request.session['sentiments'] = sentiments.to_dict()
        self.request.session['comment_sentiments'] = comment_sentiments
        
        return HttpResponseRedirect(reverse('post_analysis_output'))  # Use the name of the URL pattern

import math
from datetime import datetime

import os
import requests
from django.conf import settings


def posts_analysis_output_view(request):
    num_pics_int = request.session['num_pics']
    if num_pics_int == 0:    
        num_pics =  range(request.session['num_pics']+1)
    else:
         num_pics =  range(request.session['num_pics'])
    owner = request.session['owner']
    thumbnial_url = request.session['thumbnial_url']
    caption = request.session['caption']
    icon_url = request.session['icon_url']
    top_keywords = request.session['top_keywords'] 
    MediaCount = request.session['MediaCount'] 
    followerCount = request.session['followerCount']
    followingCount = request.session['followingCount']
    publishedAt = request.session['publishedAt']
    LikeCount = request.session['LikeCount']
    CommentCount = request.session['CommentCount'] 
    
    CommentDate = request.session['CommentDate']
    CommentLikes = request.session['CommentLikes']
    
    sentiments = request.session['sentiments']
    comment_sentiments = request.session['comment_sentiments']
    
    output_data = {
        "CommentDate": CommentDate,
        "CommentLikes": CommentLikes,
        "sentiments": sentiments,
        'top_keywords': top_keywords,
        'num_pics': num_pics_int
    }
    
    json_data = json.dumps(output_data)
    context= {
        'num_pics': num_pics,
        'caption': caption,
        'owner': owner,
        'thumbnial_url': thumbnial_url,
        'icon_url': icon_url,
        'top_keywords': top_keywords,
        "MediaCount": MediaCount,
        "followerCount": followerCount,
        "followingCount": followingCount,
        "publishedAt": publishedAt,
        "LikeCount": LikeCount,
        "CommentCount": CommentCount,
        "sentiments": sentiments,
        "comment_sentiments": comment_sentiments,
        "json_data": json_data,
        'docx_file': 'post_analysis.docx',

    }
    
   
    return render(request, 'instafeatures_pages/posts_analysis/posts_analysis_output.html', context)

def posts_dataset_zipped_output(request):
    # Handle the output display here
    # Retrieve the CSV data from the session
    commentDataset_csv = request.session.get('commentDataset_csv', '')
    Post_csv = request.session.get('Post_csv', '')
    # Create a zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr('commentDataset_csv.csv', commentDataset_csv)
        zip_file.writestr('Post_csv.csv', Post_csv)

    # Set up the HttpResponse
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="post_analysis_datasets.zip"'

    return response

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#Topic Trend Analysis
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

def topictrend_analysis_details(request):
    # You can add code here to fetch and process inquiries
    return render(request, 'instafeatures_pages/topictrend_analysis/topictrend_analysis_details.html')

def topictrend_analysis_output(request):
    # You can add code here to fetch and process inquiries
    return render(request, 'instafeatures_pages/topictrend_analysis/topictrend_analysis_output.html')

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
