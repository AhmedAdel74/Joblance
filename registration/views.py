from django.shortcuts import render,HttpResponse,redirect
from .models import Login
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required(login_url='login')
def HomePage(request):
    return render(request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confirm password do not match!!")
        else:

            my_user=Login(username=uname,email=email,password=pass1)
            my_user.save()
            return redirect('registration:signin')
        



    return render (request,'registration\signup.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']

        # loop through all User objects in the Login module
        for user in Login.objects.all():
            if user.username == username and user.password == password:
            # username and password exist, so return a success response
                return redirect('pages:home')
    
            # username and/or password do not exist, so return an error response
        return HttpResponse("Username or password is incorrect!")
    else:
        return render(request, 'registration\login.html')
    
def LogoutPage(request):
    logout(request)
    return redirect('login')