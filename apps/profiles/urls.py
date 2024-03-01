from django.urls import path
from .views import ProfileView,UpdateProfileView


app_name='profiles'

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('update-profile/<str:slug>/', UpdateProfileView.as_view(), name='update-profile'),
]
