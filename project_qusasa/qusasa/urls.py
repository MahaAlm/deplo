from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .admin import admin_site
from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin_site.urls),
    path('inquiries/', views.inquiries_view, name='inquiries'),
    path('base/', views.base, name='base'),
    path('login/', views.login_view, name='login'),
    path('wFeature/', views.wFeature, name='wFeature'),
    path('InstagramFeat/', views.InstagramFeat, name='InstagramFeat'),
    path('YouTubeFeat/', views.YouTubeFeat, name='YouTubeFeat'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('confirm_email/', views.confirm_email, name='confirm_email'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('competitive_analysis_details', views.competitive_analysis_details, name='competitive_analysis_details'),
    path('competitive_analysis/', views.CompetitiveAnalysisWizard.as_view(), name='competitive_analysis'),
    path('competitive_analysis/output/', views.competitive_analysis_output_view, name='competitive_analysis_output'),
    path('video_analysis_details', views.video_analysis_details, name='video_analysis_details'),
    path('video_analysis/', views.VideoAnalysisWizard.as_view(), name='video_analysis'),
    path('video_analysis/output/', views.video_analysis_output_view, name='video_analysis_output'),
    path('dataset_zipped_output/', views.dataset_zipped_output, name='dataset_zipped_output'),
    path('download_docx/<path:filename>/', views.download_docx, name='download_docx'),
    path('dataset_zipped_output_video_analysis/', views.dataset_zipped_output_video_analysis, name='dataset_zipped_output_video_analysis'),
    path('playlist_analysis_details', views.playlist_analysis_details, name='playlist_analysis_details'),
    path('playlist_analysis/', views.PlaylistAnalysisWizard.as_view(), name='playlist_analysis'),
    path('playlist_analysis/output/', views.playlist_analysis_output_view, name='playlist_analysis_output'),
    path('dataset_zipped_output_playlist/', views.playlist_dataset_zipped_output, name='playlist_dataset_zipped_output'),    
    path('channel_analysis_details', views.channel_analysis_details, name='channel_analysis_details'),
    path('channel_analysis/', views.ChannelAnalysisWizard.as_view(), name='channel_analysis'),
    path('channel_analysis/output/', views.channel_analysis_output_view, name='channel_analysis_output'),
    path('dataset_zipped_output_channel/', views.channel_dataset_zipped_output, name='channel_dataset_zipped_output'),    
    path('topic_analysis_details', views.topic_analysis_details, name='topic_analysis_details'),
    path('topic_analysis/', views.TopicAnalysisWizard.as_view(), name='topic_analysis'),
    path('topic_analysis/output/', views.topic_analysis_output_view, name='topic_analysis_output'),
    path('dataset_zipped_output_topic/', views.topic_dataset_zipped_output, name='topic_dataset_zipped_output'),    
    


    # You can add more paths for other views in the qusasa app here
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
