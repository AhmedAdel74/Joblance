from django.contrib import messages
from django.shortcuts import render,HttpResponse,redirect
from .models import Login
from django.contrib.auth import authenticate,login,logout
from .forms import SignupForm
from django.contrib.auth.models import User
# Create your views here.
# @login_required(login_url='login')
def HomePage(request):
    return render(request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        form = SignupForm(request.POST)
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        # pass2=request.POST.get('password2')
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request, 'Account created successfully!')
            return redirect('profiles:profile')
        elif uname=="":
            messages.error(request, "Username is required.")
        elif pass1=="":
            messages.error(request, "Password is required.")
        elif email=="":
            messages.error(request, "email is required.")
        elif User.objects.filter(username=uname).exists()==True:
            messages.info(request, f"We regret to inform you that the selected username or email, {uname} , is already registered in our system. We kindly request that you choose a different username and email address.")
        else:
            messages.error(request, f'Please correct the errors below.  {form.error_messages}')
    else:
        form = SignupForm()
        



    return render (request,'registration\signup.html',{'form':form})

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']

        # loop through all User objects in the Login module
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "Authentication successful. You are now logged in to the website.")
            return redirect('pages:home')
    
            # username and/or password do not exist, so return an error response
        else:
            messages.warning(request, f"Authentication failed due to either an incorrect username or password, or the non-existence of a user with the username '{username}'.")
            return render(request, 'registration\login.html')
    else:
        return render(request, 'registration\login.html')
    
def LogoutPage(request):
    logout(request)
    return redirect('login')

def checkExistUser(request):
    username = request.POST['username']
    email = request.POST['email']
    for user in Login.objects.all():
            if user.username == username or user.email == email:
            # username and password exist, so return a success response
                return True
    
            # username and/or password do not exist, so return an error response
    return False