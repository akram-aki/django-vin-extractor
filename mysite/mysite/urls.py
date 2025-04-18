"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # WebSocket “ws/image/” lives in your ASGI routing, so no need to list it here.
    # But for HTTP views you must wire them up:

    # Option A: serve your index() view directly at '/'
    path('', include('polls.urls')),      # if polls/urls.py defines the '' → index view

    # Option B: inline here
    # from polls import views
    # path('', views.index, name='home'),

    path('polls/', include('polls.urls')),  # if you still want /polls/ as well
    path('admin/', admin.site.urls),
]
