from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from qusasa.admin import admin_site


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin_site.urls),
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
    # You can add more paths for other views in the qusasa app here
]
