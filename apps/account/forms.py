from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm,UserChangeForm


User = get_user_model()
FORM_INPUT_CLASS = 'mt-2 mb-2 block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400'

class SignUpForm(UserCreationForm):

    class Meta:
        model =User
        fields = ['full_name','email','password1','password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].help_text = ''
            self.fields[field_name].widget.attrs.update({'class': FORM_INPUT_CLASS})
      

class LoginForm(AuthenticationForm):
      
    class Meta:
        model = User 
        fields= ['username','password']

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['username'].widget.attrs.update({'class': FORM_INPUT_CLASS})
            self.fields['password'].widget.attrs.update({'class': FORM_INPUT_CLASS})


from django.contrib.auth.forms import PasswordChangeForm

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs.update({'class': FORM_INPUT_CLASS})
        self.fields['new_password1'].widget.attrs.update({'class': FORM_INPUT_CLASS})
        self.fields['new_password2'].widget.attrs.update({'class': FORM_INPUT_CLASS})


        # Customize the form if needed