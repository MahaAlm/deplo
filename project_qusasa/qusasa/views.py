from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm  # Import at the top
from django.contrib.auth import authenticate, login

# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'qusasa/base.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'qusasa.backends.EmailBackend'
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'qusasa/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)  # Using the EmailBackend
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a desired URL
        else:
            # Invalid email or password
            return render(request, 'qusasa/login.html', {'error': 'Invalid email or password.'})
    return render(request, 'qusasa/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')