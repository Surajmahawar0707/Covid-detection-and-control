from django import forms
from .models import data, usercreatemodel


class usercreateform(forms.ModelForm):
    class Meta:
        model = usercreatemodel
        fields = ("picture", "address", "contact", "email", "district", "state", "country")

class dataform(forms.ModelForm):
    class Meta:
        model = data
        fields = ("symptoms", "contact_tracing")