from .models import Profile
from django.forms import ModelForm


class ProfileForm(ModelForm):
    FORM_INPUT_CLASS = 'mt-2 mb-2 block w-full border border-gray-300 px-4 py-3 text-gray-600 text-sm rounded focus:ring-0 focus:border-primary placeholder-gray-400'

    class Meta:
        model = Profile
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].help_text = ''
            self.fields[field_name].widget.attrs.update({'class': ProfileForm.FORM_INPUT_CLASS})
