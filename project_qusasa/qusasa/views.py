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
def features_details_view(request):
    # You can add code here to fetch and process inquiries
    return render(request, 'features_pages/feature_details.html')

from django.http import HttpResponseRedirect
from formtools.wizard.views import SessionWizardView
from .forms import CompetitiveAnalysisTypeForm, myChannelPlaylistInputForm, YouTubeSearchForm, YouTubeCategorySearchForm, ChannelsListInput, FindInitialChoiceForm, OutputChoiceForm
from django.forms import formset_factory

class CompetitiveAnalysisWizard(SessionWizardView):
    form_list = [CompetitiveAnalysisTypeForm, myChannelPlaylistInputForm, FindInitialChoiceForm, ChannelsListInput, OutputChoiceForm]
    template_name = 'features_pages/competitive_analysis.html'
    
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
        # Redirect to a new URL:
        return HttpResponseRedirect(reverse('competitive_analysis_output'))  # Use the name of the URL pattern


# URL pattern would look something like this:
# path('analysis/', AnalysisWizard.as_view())

def competitive_analysis_output_view(request):
    # Handle the output display here
    return render(request, 'features_pages/competitive_analysis_output.html')

