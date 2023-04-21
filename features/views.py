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