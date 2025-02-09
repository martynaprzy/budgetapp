from django.contrib import admin
from django.urls import path, include
from expenses.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('expenses.urls')),  
    path('', home)
]