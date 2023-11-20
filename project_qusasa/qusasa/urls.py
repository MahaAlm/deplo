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
    path('competitive_analysis_details', views.competitive_analysis_details, name='competitive_analysis_details'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('confirm_email/', views.confirm_email, name='confirm_email'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('competitive_analysis/', views.CompetitiveAnalysisWizard.as_view(), name='competitive_analysis'),
    path('competitive_analysis/output/', views.competitive_analysis_output_view, name='competitive_analysis_output'),
    path('dataset_zipped_output/', views.dataset_zipped_output, name='dataset_zipped_output'),
    
    
    


    # You can add more paths for other views in the qusasa app here
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
