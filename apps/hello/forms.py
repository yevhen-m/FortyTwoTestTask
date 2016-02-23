from django.forms import ModelForm, ImageField, FileInput, DateField

from .widgets import CalendarWidget
from .models import Profile


class ProfileForm(ModelForm):
    date_of_birth = DateField(
        widget=CalendarWidget(
            params={
                'dateFormat': '"yy-mm-dd"',
                'changeYear': 'true',
                'changeMonth': 'true',
                'yearRange': '"1950:2016"'
            },
            attrs={'class': 'datepicker'}
        )
    )
    photo = ImageField(
        label='Photo:',
        required=False,
        error_messages={'invalid': 'Image files only'},
        widget=FileInput
    )

    class Meta:
        model = Profile
        fields = '__all__'
