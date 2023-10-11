from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # You can add more paths for other views in the qusasa app here
]
