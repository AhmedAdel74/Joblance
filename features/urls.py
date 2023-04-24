from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'features'
urlpatterns = [
    path('members/', views.members, name='members'),
    path('craftsmen/', views.craftsmen, name='craftsmen'),
    path('AboutUs/', views.about_us, name='AboutUs'),
    path('career/', views.career, name='career'),
    path('interview/', views.interview, name='interview'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
