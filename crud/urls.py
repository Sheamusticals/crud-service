from django.urls import path

from .views import dynamic_model_view

urlpatterns = [
    path('overview/',dynamic_model_view),
]