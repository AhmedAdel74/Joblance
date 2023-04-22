from django.forms import SlugField
from django.shortcuts import render, redirect
from .models import Job
from django.core.paginator import Paginator
from .form import ApplyForm, JobForm
from django.urls import reverse
from .filters import JobFilter
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
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
            myform = apply_form.save(commit=False)
            myform.job = job_details
            myform.save()

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
class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('jobs:job_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)