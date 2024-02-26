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
    path('user_inquiries/', views.user_inquiries_view, name='user_inquiries'),
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
    
    
    path('download_docx/<path:filename>/', views.download_docx, name='download_docx'),

    path('competitive_analysis_details', views.competitive_analysis_details, name='competitive_analysis_details'),
    path('competitive_analysis_detail/<int:history_id>/', views.competitive_analysis_detail, name='competitive_analysis_detail'),
    path('competitive_analysis/', views.CompetitiveAnalysisWizard.as_view(), name='competitive_analysis'),
    path('competitive_analysis_redo/<int:history_id>', views.CompetitiveAnalysisWizard.as_view(), name='competitive_analysis_redo'),
    path('competitive_analysis/output/', views.competitive_analysis_output_view, name='competitive_analysis_output'),
    path('dataset_zipped_output/', views.dataset_zipped_output, name='dataset_zipped_output'),

    
    path('video_analysis_details', views.video_analysis_details, name='video_analysis_details'),
    path('video_analysis_detail/<int:history_id>/', views.video_analysis_detail, name='video_analysis_detail'),
    path('video_analysis/', views.VideoAnalysisWizard.as_view(), name='video_analysis'),
    path('video_analysis_redo/<int:history_id>', views.VideoAnalysisWizard.as_view(), name='video_analysis_redo'),
    path('video_analysis/output/', views.video_analysis_output_view, name='video_analysis_output'),
    path('dataset_zipped_output_video_analysis/', views.dataset_zipped_output_video_analysis, name='dataset_zipped_output_video_analysis'),
   
    
    path('playlist_analysis_details', views.playlist_analysis_details, name='playlist_analysis_details'),
    path('playlist_analysis_detail/<int:history_id>/', views.playlist_analysis_detail, name='playlist_analysis_detail'),
    path('playlist_analysis/', views.PlaylistAnalysisWizard.as_view(), name='playlist_analysis'),
    path('playlist_analysis_redo/<int:history_id>', views.PlaylistAnalysisWizard.as_view(), name='playlist_analysis_redo'),
    path('playlist_analysis/output/', views.playlist_analysis_output_view, name='playlist_analysis_output'),
    path('dataset_zipped_output_playlist/', views.playlist_dataset_zipped_output, name='playlist_dataset_zipped_output'),    
    
    path('channel_analysis_details', views.channel_analysis_details, name='channel_analysis_details'),
    path('channel_analysis_detail/<int:history_id>/', views.channel_analysis_detail, name='channel_analysis_detail'),
    path('channel_analysis/', views.ChannelAnalysisWizard.as_view(), name='channel_analysis'),
    path('channel_analysis_redo/<int:history_id>', views.ChannelAnalysisWizard.as_view(), name='channel_analysis_redo'),
    path('channel_analysis/output/', views.channel_analysis_output_view, name='channel_analysis_output'),
    path('dataset_zipped_output_channel/', views.channel_dataset_zipped_output, name='channel_dataset_zipped_output'),  
    
    path('topic_analysis_details', views.topic_analysis_details, name='topic_analysis_details'),
    path('topic_analysis_detail/<int:history_id>/', views.topic_analysis_detail, name='topic_analysis_detail'),
    path('topic_analysis/', views.TopicAnalysisWizard.as_view(), name='topic_analysis'),
    path('topic_analysis_redo/<int:history_id>/', views.TopicAnalysisWizard.as_view(), name='topic_analysis_redo'),
    path('topic_analysis/output/', views.topic_analysis_output_view, name='topic_analysis_output'),
    path('dataset_zipped_output_topic/', views.topic_dataset_zipped_output, name='topic_dataset_zipped_output'),    
    
    path('doc_competitive/', views.doc_competitive, name='doc_competitive'),    
    path('doc_channel/', views.doc_channel, name='doc_channel'),   
    path('doc_playlist/', views.doc_playlist, name='doc_playlist'),   
    path('doc_topic/', views.doc_topic, name='doc_topic'),
    
    path('video_retriving_details', views.video_retriving_details, name='video_retriving_details'),
    path('video_retriving_detail/<int:history_id>/', views.video_retriving_detail, name='video_retriving_detail'),
    path('video_retriving/', views.VideoRetrivingWizard.as_view(), name='video_retriving'),
    path('video_retriving_redo/<int:history_id>', views.VideoRetrivingWizard.as_view(), name='video_retriving_redo'),
    path('video_retriving/output/', views.video_retriving_output_view, name='video_retriving_output'),
    path('dataset_zipped_output_retriving/', views.dataset_zipped_output_retriving, name='dataset_zipped_output_retriving'), 
    
    path('topic-analysis/<int:history_id>/', views.topic_analysis_detail, name='topic_analysis_detail'),
      
    path('delete_history/<str:history_type>/<int:history_id>/', views.delete_history, name='delete_history'),

    # path('chat/', views.chat_view, name='chat_view'),
    path('delete_selected_templates/', views.delete_selected_templates, name='delete_selected_templates'),

  
    path('posts_analysis_details', views.posts_analysis_details, name='posts_analysis_details'),  
    path('posts_analysis_detail/<int:history_id>/', views.posts_analysis_detail, name='posts_analysis_detail'),
    path('post_analysis/', views.PostAnalysisWizard.as_view(), name='post_analysis'),
    path('post_analysis_redo/<int:history_id>', views.PostAnalysisWizard.as_view(), name='post_analysis_redo'),
    path('post_analysis/output/', views.posts_analysis_output_view, name='post_analysis_output'),
    path('dataset_zipped_output_post/', views.posts_dataset_zipped_output, name='post_dataset_zipped_output'),
    path('doc_post/', views.doc_post, name='doc_post'),
    
    path('topictrend_analysis_details/', views.topictrend_analysis_details, name='topictrend_analysis_details'),  
    path('topictrend_analysis_detail/<int:history_id>/', views.topictrend_analysis_detail, name='posts_analysis_detail'),
    path('topictrend_analysis/', views.TopicTrendAnalysisWizard.as_view(), name='topictrend_analysis'),
    path('topictrend_analysis_redo/<int:history_id>', views.TopicTrendAnalysisWizard.as_view(), name='post_analysis_redo'),
    path('topictrend_analysis_output/', views.topictrend_analysis_output, name='topictrend_analysis_output'),

    path('profile_analysis_details', views.profile_analysis_details, name='profile_analysis_details'), 
    path('profile_analysis_forms', views.ProfileAnalysisWizard.as_view(), name='profile_analysis_forms'), 
    path('profile_analysis_output', views.profile_analysis_output, name='profile_analysis_output'),

    path('people_analytics_details', views.people_analytics_details, name='people_analytics_details'), 
    
    path('comparative_study_details', views.comparative_study_details, name='comparative_study_details'), 
    
    path('instagram_reporting_details', views.instagram_reporting_details, name='instagram_reporting_details'),
    
    
    path('display_inquiry/<int:history_id>/', views.display_inquiry, name='display_inquiry'),


]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
