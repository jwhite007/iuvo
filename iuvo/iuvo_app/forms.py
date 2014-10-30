from django.forms import ModelForm, CharField, ChoiceField
from iuvo_app.models import Event, Contact
from django import forms


class ContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone_str', 'description']


class EventForm(ModelForm):
    def __init__(self, current_user, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['contacts'].queryset = self.fields['contacts'].queryset.filter(owner_id=current_user.id)

    tzchoices = [
        ('US/Hawaii', 'US/Hawaii'),
        ('US/Alaska', 'US/Alaska'),
        ('US/Pacific', 'US/Pacific'),
        ('US/Mountain', 'US/Moutain'),
        ('US/Arizona', 'US/Arizona'),
        ('US/Central', 'US/Central'),
        ('US/Eastern', 'US/Eastern'),
    ]
    timezone = ChoiceField(choices=tzchoices)


    class Meta:
        model = Event
        fields = [
            'title', 'location', 'start_day', 'start_time',
            'end_day', 'end_time', 'notify_day', 'notify_time',
            'timezone', 'contacts', 'message']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
