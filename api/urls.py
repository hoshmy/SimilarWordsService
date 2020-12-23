from django.urls import path

from . import views

urlpatterns = [
    path('v1/similar', views.similar, name='similar'),
    path('v1/stats', views.stats, name='stats'),
]