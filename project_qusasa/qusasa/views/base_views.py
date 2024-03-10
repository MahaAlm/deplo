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
from ..models import TopicAnalysisHistory, VideoAnalysisHistory, PlaylistAnalysisHistory, ChannelAnalysisHistory, VideoRetrievingHistory, CompetitiveAnalysisHistory, Inquiry
import openai
import pandas as pd
from .auth_views import *
from django.http import FileResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

##Maha's inquiry imports
from django.views.generic import ListView
def home(request):
    return render(request, 'qusasa/home.html')

@login_required
@email_verified_required
def base(request):
    topic_histories = TopicAnalysisHistory.objects.filter(user=request.user).order_by('-created_at')
    video_histories = VideoAnalysisHistory.objects.filter(user=request.user).order_by('-created_at')
    playlist_histories = PlaylistAnalysisHistory.objects.filter(user=request.user).order_by('-created_at')
    channel_histories = ChannelAnalysisHistory.objects.filter(user=request.user).order_by('-created_at')
    video_retrieving_histories = VideoRetrievingHistory.objects.filter(user=request.user).order_by('-created_at')
    competitive_histories = CompetitiveAnalysisHistory.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'qusasa/base.html', {
        'topic_histories': topic_histories,
        'video_histories': video_histories,
        'playlist_histories': playlist_histories,
        'channel_histories': channel_histories,
        'video_retrieving_histories': video_retrieving_histories,
        'competitive_histories': competitive_histories,
    })

class InqListView(ListView):
    model=Inquiry
    template_name='qusasa'

def Inq(request):

    context={
        'posts':Inquiry.objects.all()

    }
    return render(request, 'admin/inquiries.html', context)
    



def download_docx(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'documents', filename)

    if not os.path.exists(file_path):
        raise Http404("File not found.")

    try:
        fh = open(file_path, 'rb')
        response = FileResponse(fh, as_attachment=True, filename=filename)
        return response
    except Exception as e:
        raise Http404(f"An error occurred: {str(e)}")

def get_model_by_type(history_type):
    if history_type == 'video':
        return VideoAnalysisHistory
    elif history_type == 'topic':
        return TopicAnalysisHistory
    elif history_type == 'playlist':
        return PlaylistAnalysisHistory
    elif history_type == 'channel':
        return ChannelAnalysisHistory
    elif history_type == 'video_retrieving':
        return VideoRetrievingHistory
    elif history_type == 'competitive':
        return CompetitiveAnalysisHistory
    else:
        raise ValueError("Unknown history type")

def delete_history(request, history_type, history_id):
    model = get_model_by_type(history_type)
    history = get_object_or_404(model, pk=history_id, user=request.user)
    history.delete()
    return redirect('base')  # Redirect to an appropriate page


@csrf_exempt
def delete_selected_templates(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_items = data.get('selectedItems', [])

        for item in selected_items:
            model = get_model_by_type(item['type'])
            model.objects.filter(id=item['id']).delete()

        return JsonResponse({'status': 'success', 'message': 'Templates deleted successfully.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
