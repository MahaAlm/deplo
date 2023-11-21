from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm  # Import at the top
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from .utils import searchByQuery, extractIdFromUrl, analyse_channels, video_analysis
from .youtube_api import get_youtube_client




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

def home(request):
    return render(request, 'qusasa/home.html')

@login_required
@email_verified_required
def base(request):
    return render(request, 'qusasa/base.html')

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
    # You can add code here to fetch and process inquiries
    return render(request, 'qusasa/inquiries.html')

@login_required
def competitive_analysis_details(request):
    # You can add code here to fetch and process inquiries
    return render(request, 'features_pages/competitive_analysis/competitive_analysis_details.html')

from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from .forms import CompetitiveAnalysisTypeForm, myChannelPlaylistInputForm, YouTubeSearchForm, YouTubeCategorySearchForm, ChannelsListInput, FindInitialChoiceForm

class CompetitiveAnalysisWizard(SessionWizardView):
    form_list = [CompetitiveAnalysisTypeForm, myChannelPlaylistInputForm, FindInitialChoiceForm, ChannelsListInput]
    template_name = 'features_pages/competitive_analysis/competitive_analysis.html'
    
    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)
        # If it's the step that needs conditional logic to pick the form.
        if step == '3':
            previous_choice = self.get_cleaned_data_for_step('2')['choice']  # '1' is the step for FindInitialChoiceForm
            if previous_choice == 'input_list':
                self.form_list[step] = ChannelsListInput 
                form = ChannelsListInput(data, files, prefix=self.get_form_prefix(step, ChannelsListInput))
            elif previous_choice == 'search':
                self.form_list[step] = YouTubeSearchForm 
                form = YouTubeSearchForm(data, files, prefix=self.get_form_prefix(step, YouTubeSearchForm))
            elif previous_choice == 'category':
                self.form_list[step] = YouTubeCategorySearchForm 
                form = YouTubeCategorySearchForm(data, files, prefix=self.get_form_prefix(step, YouTubeCategorySearchForm))
        return form


    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        # Determine the current step. If it's the second form, change the label dynamically
        if self.steps.current == '1':  # assuming '1' is the index of InputForm
            previous_data = self.get_cleaned_data_for_step('0') or {}
            analysis_type = previous_data.get('analysis_type')
            if analysis_type == 'channels':
                form.fields['input_text'].label = 'channel'
            elif analysis_type == 'playlists':
                form.fields['input_text'].label = 'playlist'
        
        if self.steps.current == '3':
            context['step2_data'] = self.get_cleaned_data_for_step('2') or {}
        return context
    
    
    def done(self, form_list, **kwargs):
        # Process the cleaned data
        cleaned_data = self.get_all_cleaned_data()
        
        # Do something with the data and generate dataset/report as required
        entity_type = cleaned_data.get('analysis_type')
        my_link = cleaned_data.get('input_text')
        search_or_list = cleaned_data.get('choice') #('input_list', 'search')
        print()
        youtube = get_youtube_client()
        
        if(search_or_list == 'search'):
            search = True
            query = cleaned_data.get('search_query')
            order = cleaned_data.get('order')
            region_code = cleaned_data.get('region_code')
            language = cleaned_data.get('language')
            ids_list = searchByQuery(youtube, query, entity_type, order, region_code, language)
            ids_list.insert(0, extractIdFromUrl(my_link))
            
        elif(search_or_list == 'input_list'):
            ids_list = []
            ids_list.append(my_link)
            ids_list.append(extractIdFromUrl(cleaned_data.get('channel_url_1')))
            ids_list.append(extractIdFromUrl(cleaned_data.get('channel_url_2')))
            ids_list.append(extractIdFromUrl(cleaned_data.get('channel_url_3')))
            ids_list.append(extractIdFromUrl(cleaned_data.get('channel_url_4')))
        
        print(ids_list)
        channel_data_df, top_videos_df, channel_icons, durations_list = analyse_channels(ids_list, entity_type, youtube)
        
        channel_data_csv = channel_data_df.to_csv(index=False)
        top_videos_csv = top_videos_df.to_csv(index=False)
        # Extract channel names
        print(channel_data_df.columns)
        channel_names = channel_data_df['Name'].tolist()
        
        top_videos_dict = top_videos_df.to_dict(orient='records')
        self.request.session['top_videos'] = top_videos_dict

        

        # Store in session
        self.request.session['channel_icons'] = channel_icons
        self.request.session['channel_names'] = channel_names
        self.request.session['channel_data_csv'] = channel_data_csv
        self.request.session['top_videos_csv'] = top_videos_csv
        self.request.session['durations'] = durations_list
        
        average_likes = channel_data_df['Like average'].tolist()
        top_likes_channel = channel_data_df.sort_values('Like average', ascending=False)['Name'].iloc[0]
        
        average_views = channel_data_df['View average'].tolist()
        top_views_channel = channel_data_df.sort_values('View average', ascending=False)['Name'].iloc[0]

        subs = channel_data_df['Subscriber count'].tolist()
        top_subs_channel = channel_data_df.sort_values('Subscriber count', ascending=False)['Name'].iloc[0]

        mostUsedCategories = channel_data_df['mostUsedCategories'].tolist()
        topTags = channel_data_df['Top tags'].tolist()
        
        self.request.session['mostUsedCategories'] = mostUsedCategories
        self.request.session['topTags'] = topTags
        self.request.session['average_likes'] = average_likes
        self.request.session['top_likes_channel'] = top_likes_channel
        self.request.session['average_views'] = average_views
        self.request.session['top_views_channel'] = top_views_channel
        self.request.session['subs'] = subs
        self.request.session['top_subs_channel'] = top_subs_channel
        self.request.session['type'] = entity_type
        self.request.session['durations'] = durations_list
        # Redirect to a new URL:
        return HttpResponseRedirect(reverse('competitive_analysis_output'))  # Use the name of the URL pattern


# URL pattern would look something like this:
# path('analysis/', AnalysisWizard.as_view())
import json

def competitive_analysis_output_view(request):
    channel_icons = request.session.get('channel_icons', [])
    channel_names = request.session.get('channel_names', [])
    top_videos = request.session.get('top_videos', [])
    durations = request.session.get('durations', [])
    output_data = {
        'average_likes': request.session['average_likes'],
        'average_views': request.session['average_views'],
        'subs': request.session['subs'],
        'channel_names': channel_names,
        'durations': durations,
        'mostUsedCategories': request.session.get('mostUsedCategories', []),
        'topTags': request.session.get('topTags', []),
    }
    json_data = json.dumps(output_data)
    

    # Zip the lists together in the view
    channels = zip(channel_icons, channel_names)
    channels_tags = zip(request.session.get('topTags', []), channel_names)
    context = {
        'channels': channels,
        'json_data': json_data,
        'top_likes_channel': request.session['top_likes_channel'],
        'top_views_channel': request.session['top_views_channel'],
        'top_subs_channel': request.session['top_subs_channel'],
        'type': request.session['type'],
        'top_videos': top_videos,
        'output_data': output_data,
        'channels_tags': channels_tags
        
    }
    return render(request, 'features_pages/competitive_analysis/competitive_analysis_output.html', context)



@login_required
def video_analysis_details(request):
    # You can add code here to fetch and process inquiries
    return render(request, 'features_pages/video_analysis/video_analysis_details.html')

from .forms import VideoAnalysisInputForm

class VideoAnalysisWizard(SessionWizardView):
    form_list = [VideoAnalysisInputForm]
    template_name = 'features_pages/video_analysis/video_analysis_forms.html'  
    
    def done(self, form_list, **kwargs):
        # Process the cleaned data
        youtube = get_youtube_client()
        cleaned_data = self.get_all_cleaned_data()
        video_url = cleaned_data.get('video_url')
        video_id = extractIdFromUrl(video_url)
        video_info_df, comments_df, emotion_counts, top_comments_by_emotion = video_analysis(youtube, video_id)
        
        video_info_csv = video_info_df.to_csv(index=False)
        comments_csv = comments_df.to_csv(index=False)
        
        self.request.session['video_info_csv'] = video_info_csv
        self.request.session['comments_csv'] = comments_csv
        
        self.request.session['emotion_counts'] = emotion_counts
        self.request.session['top_comments_by_emotion'] = top_comments_by_emotion
        return HttpResponseRedirect(reverse('video_analysis_output'))  # Use the name of the URL pattern


def video_analysis_output_view(request):
    
    output_data = {
        'emotion_counts': request.session['emotion_counts'],
        'top_comments_by_emotion': request.session['top_comments_by_emotion'],
    }
    
    json_data = json.dumps(output_data)
    
    context= {json_data}
    
    return render(request, 'features_pages/video_analysis/video_analysis_output.html', context)



import zipfile
import io

def dataset_zipped_output_video_analysis(request):
    # Handle the output display here
    # Retrieve the CSV data from the session
    video_info_csv = request.session.get('video_info_csv', '')
    comments_csv = request.session.get('comments_csv', '')
    # Create a zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr('video_info_csv.csv', video_info_csv)
        zip_file.writestr('comments_csv.csv', comments_csv)

    # Set up the HttpResponse
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="video_analysis_datasets.zip"'

    return response

def dataset_zipped_output(request):
    # Handle the output display here
    # Retrieve the CSV data from the session
    channel_data_csv = request.session.get('channel_data_csv', '')
    top_videos_csv = request.session.get('top_videos_csv', '')
    # Create a zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr('channel_data.csv', channel_data_csv)
        zip_file.writestr('top_videos.csv', top_videos_csv)

    # Set up the HttpResponse
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="data.zip"'

    return response


