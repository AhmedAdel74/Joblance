from django.shortcuts import render
from .models import Job

# Create your views here.

def jobs_list(request):

    jobs_list = Job.objects.all()
    context = {'jobs': jobs_list}
    return render(request,'job/jobs_list.html',context)



def job_details(request, id):
    pass