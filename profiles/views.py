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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

@login_required()
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render( request ,  'profiles/profile.html' ,{'profile':profile})



@login_required()
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
    success_url = reverse_lazy('password_change_done')
    # New Password Admin1990

    # spider admin5555
    # spider (newpassword) admin7777










        #Sharaf Section
def others(request):
    others      = Profile.objects.all()
    paginator   = Paginator(others,12)
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)
    context     = {'users' : page_obj }
    return render(request,'profiles/others.html',context)

def other(request, id):
    profile = get_object_or_404(Profile, id=id)
    return render(request,'profiles/other.html',{'user' : profile}) 


def search(request):
    query = request.GET.get('q')
    results = []
    if query:
        query_list = query.split()
        # Use the Q object to create a query that searches for the query string
        # across multiple fields
        results = Profile.objects.filter(
            Q(fname__icontains=query_list[0]) |
            Q(lname__icontains=query_list[0]) |
            Q(email__icontains=query_list[0])
        ).distinct()
        for word in query_list[1:]:
            results = results.filter(
                Q(fname__icontains=word) |
                Q(lname__icontains=word) |
                Q(email__icontains=word)
            ).distinct()
    return render(request, 'profiles/search.html', {'query': query, 'results': results})
