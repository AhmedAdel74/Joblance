from django.forms import SlugField
from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Apply
from django.core.paginator import Paginator
from .form import ApplyForm, JobForm
from django.urls import reverse
from .filters import JobFilter
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.


def jobs_list(request):

    jobs_list = Job.objects.all()

    # filters
    myfilter = JobFilter(request.GET, queryset=jobs_list)
    jobs_list = myfilter.qs

    paginator = Paginator(jobs_list, 5)  # Show 5 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'jobs': page_obj,
               'forcount': jobs_list,
               'myfilter': myfilter,
               }
    return render(request, 'job/jobs_list.html', context)


@login_required()
def job_details(request, slug):
    job_details = Job.objects.get(slug=slug)

    if request.method == 'POST':
        apply_form = ApplyForm(request.POST, request.FILES)
        if apply_form.is_valid():
            application = apply_form.save(commit=False)
            application.job = job_details
            application.applicant = request.user
            application.save()

    else:
        apply_form = ApplyForm()

    context = {'job': job_details, 'apply_form': apply_form}
    return render(request, 'job\job_details.html', context)


@login_required()
def add_job(request):
    if request.method == 'POST':
        post_form = JobForm(request.POST, request.FILES)
        if post_form.is_valid():
            myform = post_form.save(commit=False)
            myform.owner = request.user
            myform.save()
            return redirect(reverse('jobs:job_list'))

    else:
        post_form = JobForm()

    return render(request, 'job/add_job.html', {'post_form': post_form})


@login_required()
def edit_job(request, id):
    job = Job.objects.get(id=id)
    if job.owner != request.user:
        # If the user is not the creator of the job, return a 403 error
        return redirect('pages:home')
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('jobs:job_list')
    else:
        form = JobForm(instance=job)
    context = {'job': job, 'form': form}
    return render(request, 'job\edit_job.html', context)


@login_required()
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.user == job.owner:
        job.delete()
    return redirect('jobs:job_list')

@login_required()
def your_jobs(request):
    jobs_list = Job.objects.filter(owner=request.user)
    applications = Apply.objects.filter(job__in=jobs_list).select_related('applicant')

    myfilter = JobFilter(request.GET, queryset=jobs_list)
    jobs_list = myfilter.qs

    paginator = Paginator(jobs_list, 5)  # Show 5 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'jobs': page_obj,
               'forcount': jobs_list,
               'myfilter': myfilter,
               'applications': applications,
               }
    return render(request, 'job/your_jobs.html', context)