from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django_countries.fields import CountryField
from .models import *


class ContactForm(forms.Form):
    class Meta:
        widgets = {
            'phone': PhoneNumberPrefixWidget(initial='US'),
        }


class ProfileForm(forms.Form):
    phone = ContactForm
    addressLine1 = forms.CharField(
        required=True,
        label='Address Line 1',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Address Line 1'}))
    addressLine2 = forms.CharField(
        required=False,
        label='Address Line 2',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Address Line 2'}))
    city = forms.CharField(
        required=True,
        label='City',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Your City'}))
    state = forms.CharField(
        required=True,
        label='State',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Your State'}))
    countries = CountryField().formfield()
    zipCode = forms.CharField(
        required=True,
        label='Zip Code',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Your State'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('addressLine1', css_class='form-group col-md-6'),
                Column('addressLine2', css_class='form-group col-md-6')
            ),
            Row(
                Column('city', css_class='form-group col-md-6'),
                Column('state', css_class='form-group col-md-6')
            ),
            Row(
                Column('countries', css_class='form-group col-md-6'),
                Column('zipCode', css_class='form-group col-md-6')
            ),
            Row(
                Column('phone', css_class='form-group col-md-6'),
            ),
            Submit('submit', 'Save Changes', css_class='btn btn primary me-2')
        )

    class Meta:
        model = Profile
        fields = ['addressLine1', 'addressLine2',
                  'city', 'state', 'countries', 'zipCode', 'phone']
