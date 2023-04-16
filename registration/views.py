from django.contrib import messages
from django.shortcuts import render,HttpResponse,redirect
from .models import Login
from django.contrib.auth import authenticate,login,logout

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

        if uname=="":
            messages.error(request, "Username is required.")
        elif pass1=="":
            messages.error(request, "Password is required.")
        elif email=="":
            messages.error(request, "email is required.")
        elif checkExistUser(request)==True:
            messages.info(request, f"We regret to inform you that the selected username or email, {uname} , is already registered in our system. We kindly request that you choose a different username and email address.")
        elif pass1!=pass2:
            messages.warning(request, "Your password and confirm password do not match!!")
        else:

            my_user=Login(username=uname,email=email,password=pass1)
            my_user.save()
            messages.success(request, "The registration on the site was successful.")
            return redirect('registration:signin')
        



    return render (request,'registration\signup.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']

        # loop through all User objects in the Login module
        for user in Login.objects.all():
            if (user.username == username or user.email==username) and user.password == password :#and (username != "" or password!="")
            # username and password exist, so return a success response
                messages.success(request, "Authentication successful. You are now logged in to the website.")
                return redirect('pages:home')
    
            # username and/or password do not exist, so return an error response
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