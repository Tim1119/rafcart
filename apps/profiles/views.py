from django.shortcuts import render,get_object_or_404
from django.views.generic import UpdateView,TemplateView
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
# Create your views here.


class ProfileView(LoginRequiredMixin,TemplateView):
    model = Profile
    template_name = 'profiles/profile.html'
          
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile =  get_object_or_404(Profile,user=self.request.user) 
        context['profile'] = profile
        return context


class UpdateProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/update_profile.html'
    success_url = reverse_lazy('profiles:profile')
    success_message = 'Your profile was updated succesfully'

    def get_object(self, queryset=None):
        obj = super(UpdateProfileView, self).get_object()
        if not obj.user == self.request.user:
            raise PermissionDenied(
                "You don't have permission to update a profile that's not yours")
        return obj
