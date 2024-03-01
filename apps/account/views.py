from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm
from .tasks import send_activation_email
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect
from .forms import LoginForm,ChangePasswordForm
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy



User = get_user_model()

class SignUpView(SuccessMessageMixin,CreateView):
    template_name = 'account/pages/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('account:login')
    success_message='Account successfully created'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  
        user.save()
        current_site = get_current_site(self.request)
        send_activation_email.delay(user_id=user.id,domain=current_site.domain)
        return super().form_valid(form)

      
class ActivateAccount(View):
    

    def get(request,uidb64,token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request,message='Account Activation Successful')
            return redirect('account:login')
        else:
            messages.success(request,message='Activation Link is Invalid')
            return redirect('accounts:login')


class LoginUserView(SuccessMessageMixin,LoginView):
    template_name = 'account/pages/login.html'
    authentication_form = LoginForm
    success_message='Account successfully logged in'
    next_page = reverse_lazy('account:login')

class LogoutUserView(SuccessMessageMixin,LoginRequiredMixin,LogoutView):
    next_page = reverse_lazy('account:login')
    success_message='Account logged out successfully'



class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('account:login')
    template_name = 'account/pages/change_password.html'