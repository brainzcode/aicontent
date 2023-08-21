from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
# from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django_countries.fields import CountryField
from .models import *


# class ContactForm(forms.ModelForm):
#     class Meta:
#         widgets = {
#             'phone': PhoneNumberPrefixWidget(initial='US'),
#         }


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        label='Firstname',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Firstname'}))
    last_name = forms.CharField(
        required=True,
        label='Lastname',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Lastname'}))
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
    # country = forms.CharField(
    #     required=True, label='Country',
    #     widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Your Country'}))
    country = forms.ChoiceField(
        required=True, label='Country', choices=COUNTRIES, widget=forms.Select(), initial='Select Country')
    zipCode = forms.CharField(
        required=True,
        label='Zip Code',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Your State'}))
    phone_number = forms.CharField(
        required=True,
        label='Phone Number',
        widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter Your Number'}
                               ))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(Field('first_name', value=self.user.first_name),
                       css_class='form-group col-md-6'),
                Column(Field('last_name', value=self.user.last_name),
                       css_class='form-group col-md-6')
            ),
            Row(
                Column('addressLine1', css_class='form-group col-md-6'),
                Column('addressLine2', css_class='form-group col-md-6')
            ),
            Row(
                Column('city', css_class='form-group col-md-6'),
                Column('state', css_class='form-group col-md-6')
            ),
            Row(
                Column('country', css_class='form-group col-md-6'),
                Column('zipCode', css_class='form-group col-md-6')
            ),
            Row(
                Column('phone_number', css_class='form-group col-md-12')
            ),
            Submit('submit', 'Save Changes',
                   css_class='btn btn primary me-2 mb-3')
        )

    class Meta:
        model = Profile
        fields = ['addressLine1', 'addressLine2',
                  'city', 'state', 'country', 'zipCode', 'phone_number']

    def save(self, *args, **kwargs):
        user = self.instance.user
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        profile = super(ProfileForm, self).save(*args, **kwargs)
        return profile


class ProfileImageForm(forms.ModelForm):
    profileImage = forms.ImageField(
        required=True,
        label='Upload Profile Image',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['profileImage',]
