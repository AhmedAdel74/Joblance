import datetime
from audioop import reverse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserForm,ProfileForm 
from .models import Profile
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.


def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render( request ,  'profiles/profile.html' ,{'profile':profile})




def edite(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        print("No Profile")
        profile = None
    #userform = UserForm()
    #profileform=ProfileForm()
    if request.method=='POST':
        userform= UserForm(request.POST,request.FILES, instance=request.user)
        profileform =ProfileForm(request.POST ,request.FILES, instance= profile)
        #date_profile = validated_data['dob']
        #transformed_date = datetime.datetime.strptime(date_profile, '%m/%d/%Y').strftime('%Y-%m-%d')
        #print(date_profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            print("Saved")
            #myprofile=profileform.save()
            ## لو التاريخ فيه مشكلة فى ترتيب الشهور والايام
            ## حوليه قبل ما يتحفظ
            ## بالسطر دة
            #print(myprofile.dob)
            # دة لتحويل التاريخ ل str
            #date_in_str = str(myprofile.dob)
            # دة لتحويله من صيغة الى صيغة تانية
            # تكتب فى strptime الصيغة اللى ها تحولى منها
            # فى strftime الصيغة الى ها تحولى ليها
            #transformed_date = datetime.datetime.strptime(date_in_str, '%m/%d/%Y').strftime('%Y-%m-%d')
            #transformed_date = str(transformed_date)
            #print(transformed_date)
            return redirect('profiles:profile')
        else:
            print("Error In Saved")
            print(profileform.errors)
            userform =UserForm(instance=request.user)
            profileform=ProfileForm(instance=profile)
    else:
        userform =UserForm(instance=request.user)
        profileform=ProfileForm(instance=profile)
        
    return render(request , 'profiles/edite.html',
                  {
            'userform':userform ,
            'profileform':profileform })







class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'profiles/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('edite')