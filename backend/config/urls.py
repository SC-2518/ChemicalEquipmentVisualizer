from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Backend API is Running</h1><p>Use <a href='/api/'>/api/</a> for endpoints.</p>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('', home),
]
