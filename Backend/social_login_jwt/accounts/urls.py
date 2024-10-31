from django.urls import path
from .views import *

urlpatterns = [
    path('google-login/', LoginWithGoogle.as_view()),
]
