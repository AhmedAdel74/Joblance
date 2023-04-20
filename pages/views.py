from django.shortcuts import render
from django.urls import reverse
from .models import Info
from django.core.mail import send_mail
from django.conf import settings
from job.models import Job
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,HttpResponse,redirect

# Create your views here.

def index(request):
    jobs_list = Job.objects.all()[:6]
    context = {'jobs': jobs_list,
               }
    return render(request, 'pages/index.html', context)





def home(request):
    return render(request, 'pages/home.html')

def send_message(request):
    myinfo = Info.objects.first()
    if request.method == 'POST':
        subject = request.POST['subject']
        email = request.POST['email']
        message = request.POST['message']

        send_mail(
            email,
            message,
            email,
            [settings.EMAIL_HOST_USER],
        )

    
    return render(request, 'pages/feedback.html', {'myinfo':myinfo})

def LogoutPage(request):
    logout(request)
    home_url = reverse('pages:home')
    print(home_url)  # Add this line to print the URL
    return redirect(home_url)