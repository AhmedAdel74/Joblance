from django.urls import  path, include
from . import views

urlpatterns = [
    path('', views.jobs_list),
    path('<int:id>', views.job_details),
]
