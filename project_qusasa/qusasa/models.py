from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # remove the username field
    email = models.EmailField(unique=True, verbose_name='email address')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # removes email from REQUIRED_FIELDS
    
    is_verified = models.BooleanField(default=False)
    email_confirmation_code = models.CharField(max_length=30, blank=True, null=True)
    
    objects = CustomUserManager() 
    
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.template.loader import render_to_string

@receiver(post_save, sender=CustomUser)
def send_verification_email(sender, instance, **kwargs):
    if not instance.is_verified and not instance.email_confirmation_code:
        # Generate a unique confirmation code
        confirmation_code = generate_confirmation_code()
        instance.email_confirmation_code = confirmation_code
        instance.save()

        # Render the email content with the template
        html_message = render_to_string('registration/email_verification_template.html', {
            'confirmation_code': confirmation_code
        })

        # Send an email with the confirmation code
        send_mail(
            'Confirm your email address',
            'Use the code provided in the attached HTML to confirm your email address.',  # This is a fallback for email clients that do not support HTML
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=False,
            html_message=html_message  # This is the HTML message
        )


import random
def generate_confirmation_code(length=6):
    """Generate a random numerical confirmation code of a given length."""
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


class TopicAnalysisHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    search_query = models.CharField(max_length=200)
    order = models.CharField(max_length=50)
    region_code = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    # Add other fields as necessary
    created_at = models.DateTimeField(auto_now_add=True)
    
class VideoAnalysisHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_url = models.URLField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)

class PlaylistAnalysisHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    playlist_url = models.URLField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)

class ChannelAnalysisHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    channel_url = models.URLField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Channel Analysis for {self.channel_url} by {self.user}"
    
class VideoRetrievingHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    search_query = models.CharField(max_length=1024)
    order = models.CharField(max_length=100)
    region_code = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    num_of_videos = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video Retrieving Analysis for {self.search_query} by {self.user}"


class CompetitiveAnalysisHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    analysis_type = models.CharField(max_length=100)
    input_text = models.CharField(max_length=2048)
    choice = models.CharField(max_length=100)
    search_query = models.CharField(max_length=2048, blank=True, null=True)
    order = models.CharField(max_length=100, blank=True, null=True)
    region_code = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    channel_urls = models.JSONField(blank=True, null=True)  # For storing multiple channel URLs if needed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Competitive Analysis for {self.input_text} by {self.user}"
    


STATUS_CHOICES = (
        ('WAITING', 'Waiting'),
        ('RESOLVED', 'Resolved'),
    )
#hi
class Inquiry(models.Model):
    title= models.CharField(max_length=1000)
    InqContent=models.TextField()
    RepContent=models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    date_posted=models.DateTimeField(auto_now_add=True)
    date_resolved=models.DateTimeField()
    author= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)