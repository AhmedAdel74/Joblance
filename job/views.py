from django.shortcuts import render, redirect
from .models import Job
from django.core.paginator import Paginator
from .form import ApplyForm , JobForm
from django.urls import reverse
# Create your views here.

def jobs_list(request):

    jobs_list = Job.objects.all()

    paginator = Paginator(jobs_list, 5) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'jobs': page_obj, 
               'forcount': jobs_list}
    return render(request,'job/jobs_list.html',context)



def job_details(request, slug):
    job_details = Job.objects.get(slug = slug)

    if request.method=='POST':
        apply_form = ApplyForm(request.POST , request.FILES)
        if apply_form.is_valid():
            myform = apply_form.save(commit=False)
            myform.job = job_details
            myform.save()

    else:
        apply_form = ApplyForm()

    context = {'job': job_details, 'apply_form':apply_form}
    return render(request, 'job\job_details.html', context)

def add_job(request):
    if request.method=='POST':
        post_form = JobForm(request.POST , request.FILES)
        if post_form.is_valid():
            myform = post_form.save(commit=False)
            myform.owner = request.user
            myform.save()
            return redirect(reverse('jobs:job_list'))

    else:
        post_form = JobForm()

    return render(request,'job/add_job.html',{'post_form':post_form})