import re

from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email

from Backend import settings
from Venter.models import File, Profile

from .validate import csv_file_header_validation


class CSVForm(forms.ModelForm):
    """
    ModelForm, used to facilitate CSV file upload.

    Meta class------
        1) declares 'File' as the model class to generate the 'csv_form'
        2) includes only only field in the 'csv_form 'from the File model

    Usage:
        1) upload_file.html template: Generates the file form fields in the csv file upload page for logged in users.
    """
    class Meta:
        model = File
        fields = ('csv_file',)

    def __init__(self, *args, **kwargs):
        """
        It accepts the self.request argument, here for the purpose of accessing the logged-in user's organisation name
        """
        self.request = kwargs.pop("request")
        super(CSVForm, self).__init__(*args, **kwargs)

    def clean_csv_file(self):
        """
        It validates specific attributes of 'csv_file' field: csv header, file type, and file size.
        """

        # cleaning and retrieving the uploaded csv file to perform further validation on it
        uploaded_csv_file = self.cleaned_data['csv_file']

        # checks for non-null file upload
        if uploaded_csv_file:
            # validation of the filetype based on the extension type .csv
            # validation of the filesize based on the size limit 5MB
            # the csv_file_header_validation() is invoked from validate.py
            filename = uploaded_csv_file.name
            if filename.endswith(settings.FILE_UPLOAD_TYPE):
                if uploaded_csv_file.size < int(settings.MAX_UPLOAD_SIZE):
                    if csv_file_header_validation(uploaded_csv_file, self.request):
                        return uploaded_csv_file
                    else:
                        raise forms.ValidationError(
                            "Incorrect headers detected, please upload correct file")
                else:
                    raise forms.ValidationError(
                        "File size must not exceed 5 MB")
            else:
                raise forms.ValidationError(
                    "Please upload .csv extension files only")

        return uploaded_csv_file


class UserForm(forms.ModelForm):

    """
    Modelform, generated from Django's user model.

    Meta class------
        1) declares 'User' as the model class to generate the 'user_form'
        2) includes only five fields in the 'user_form' from the User model

    Note------
        CSS styling done per widget instance

    Usage------
        1) 'registration.html' template: Generates the user form fields in the signup page for new users
        2) 'update_profile.html' template: Generates the user form fields in the update profile page for existing users
    """
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

class ProfileForm(forms.ModelForm):
    """
    Modelform, generated from Django's Profile model.

    Meta class------
        1) declares 'Profile' as the model class to generate the 'profile_form'
        2) includes only three fields in the 'profile_form' from the Profile model

    Usage------
        1) 'registration.html' template: Generates the profile form fields in the signup page for new users
        2) 'update_profile.html' template: Generates the profile form fields in the update profile page
        for existing users
    """
    class Meta:
        model = Profile
        fields = ('phone_number', 'profile_picture')


class ContactForm(forms.Form):
    company_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=True)
    email_address = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}), required=True)
    contact_no = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=True, max_length=10)
    requirement_details = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}), required=True)

    def clean(self):
        """
        It validates specific attributes of 'contact_form' field: email, contact_no.
        """
        email_address = self.cleaned_data.get('email_address')
        contact_no = self.cleaned_data.get('contact_no')

        if validate_email(email_address):
            pattern = re.compile(r'^[6-9]\d{9}$')
            if bool(pattern.match(contact_no)):
                return self.cleaned_data
            else:
                raise forms.ValidationError(
                    "Please enter a valid phone number")