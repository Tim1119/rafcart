from django.urls import path
from .views import SignUpView, ActivateAccount,LoginUserView,LogoutUserView,ChangePasswordView


app_name='account'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('change-password/',ChangePasswordView.as_view(), name='change_password'),
]
