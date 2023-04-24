from django.shortcuts import render
from .models import Craftsmen

# Create your views here.


def members(request):
    return render(request, 'features/members.html')


def craftsmen(request):

    craftsmen_list = Craftsmen.objects.all()

    context = {'list': craftsmen_list,
               }
    return render(request, 'features/craftsmen.html', context)


def about_us(request):
    return render(request, 'features/AboutUs.html')


def career(request):
    return render(request, 'features/career.html')


def interview(request):
    return render(request, 'features/interview.html')
