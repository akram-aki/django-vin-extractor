from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),    # root URL → index()
    # (Optionally) path('api/', include('camera.urls')), etc.
]
