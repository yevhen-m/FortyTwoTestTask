from django.forms import ModelForm, ImageField, FileInput

from .models import Profile


class ProfileForm(ModelForm):
    photo = ImageField(
        label='Photo:',
        required=False,
        error_messages={'invalid': "Image files only"},
        widget=FileInput
    )

    class Meta:
        model = Profile
        fields = '__all__'
