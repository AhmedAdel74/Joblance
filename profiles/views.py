import datetime
from audioop import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProfileForm
from .models import Profile, Rate
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.urls import reverse

# Create your views here.


@login_required()
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request,  'profiles/profile.html', {'profile': profile})


@login_required()
def edite(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        print("No Profile")
        profile = None
    # userform = UserForm()
    # profileform=ProfileForm()
    if request.method == 'POST':
        userform = UserForm(request.POST, request.FILES, instance=request.user)
        profileform = ProfileForm(
            request.POST, request.FILES, instance=profile)
        # date_profile = validated_data['dob']
        # transformed_date = datetime.datetime.strptime(date_profile, '%m/%d/%Y').strftime('%Y-%m-%d')
        # print(date_profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            print("Saved")
            # myprofile=profileform.save()
            # لو التاريخ فيه مشكلة فى ترتيب الشهور والايام
            # حوليه قبل ما يتحفظ
            # بالسطر دة
            # print(myprofile.dob)
            # دة لتحويل التاريخ ل str
            # date_in_str = str(myprofile.dob)
            # دة لتحويله من صيغة الى صيغة تانية
            # تكتب فى strptime الصيغة اللى ها تحولى منها
            # فى strftime الصيغة الى ها تحولى ليها
            # transformed_date = datetime.datetime.strptime(date_in_str, '%m/%d/%Y').strftime('%Y-%m-%d')
            # transformed_date = str(transformed_date)
            # print(transformed_date)
            return redirect('profiles:profile')
        else:
            print("Error In Saved")
            print(profileform.errors)
            userform = UserForm(instance=request.user)
            profileform = ProfileForm(instance=profile)
    else:
        userform = UserForm(instance=request.user)
        profileform = ProfileForm(instance=profile)

    return render(request, 'profiles/edit.html',
                  {
                      'userform': userform,
                      'profileform': profileform})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'profiles/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('password_change_done')
    # New Password Admin1990

    # spider admin5555
    # spider (newpassword) admin7777

    # Sharaf Section


def others(request):
    query = request.GET.get('q')
    others = None
    if query:
        others = Profile.objects.filter(
            Q(user__username__icontains=query) | Q(email__icontains=query)
        )
    else:
        others = Profile.objects.all().annotate(
            average_quality=Avg('rate__RAtingQuality')
        ).order_by('-average_quality', '-id')
    
    paginator = Paginator(others, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'users': page_obj, 'query': query}
    return render(request, 'profiles/others.html', context)


def other(request, id):
    profile = Profile.objects.get(id=id)
    Revq = profile.average_quality()
    Revs = profile.average_speed()
    Revm = profile.average_moralistic()
    rating_details = Rate.objects.filter(RA_Other=profile)
    context = {'user': profile ,'rating_details': rating_details , 'RAtingQuality':Revq , 'RAtingSpeed':Revs , 'RAtingMoralistic':Revm}
    return render(request, 'profiles/other.html', context)

def submit_rating(request, rateid):
    if request.method == 'POST':
        user = request.user
        other = Profile.objects.get(id=rateid)
        quality_rating = request.POST.get('quality_rating')
        speed_rating = request.POST.get('speed_rating')
        moralistic_rating = request.POST.get('moralistic_rating')
        description = request.POST.get('description')
        existing_rating = Rate.objects.filter(RAUser=user, RA_Other=other).first()
        
        if existing_rating:
            # An existing rating was found, update it with new values
            if quality_rating is None and speed_rating is None and moralistic_rating is None and description == '':
                # No rating or description is provided, inform the user to fill in at least one of the fields
                messages.warning(request, "Please fill in at least one of the rating fields or the description field.")
            else:
                existing_rating.RAtingQuality = quality_rating
                existing_rating.RAtingSpeed = speed_rating
                existing_rating.RAtingMoralistic = moralistic_rating
                existing_rating.RADescription = description
                existing_rating.save()
                messages.success(request, "The rating has been updated successfully.")
        else:
            # No rating exists for this user and profile, create and save a new Rating object
            if quality_rating is None and speed_rating is None and moralistic_rating is None and description == '':
                # No rating or description is provided, inform the user to fill in at least one of the fields
                messages.warning(request, "Please fill in at least one of the rating fields or the description field.")
            else:
                rating = Rate(
                    RAUser=user,
                    RA_Other=other,
                    RAtingQuality=quality_rating,
                    RAtingSpeed=speed_rating,
                    RAtingMoralistic=moralistic_rating,
                    RADescription=description
                )
                rating.save()
                messages.success(request, "The evaluation of the profile has been completed successfully.")
        
        return redirect('profiles:other', id=rateid)
