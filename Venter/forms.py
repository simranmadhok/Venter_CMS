from django import forms
from django.contrib.auth.models import User

from Backend import settings
from Venter.models import File, Header, Profile


class CSVForm(forms.ModelForm):
    """
    ModelForm, used to facilitate CSV file upload.

    Usage:
        1) upload_file.html template: Generates the file form fields in the csv file upload page for logged in users.
    """
    class Meta:
        model = File
        fields = ('csv_file',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(CSVForm, self).__init__(*args, **kwargs)

    def clean_csv_file(self):
        uploaded_csv_file = self.cleaned_data['csv_file']
        if uploaded_csv_file:
            filename = uploaded_csv_file.name

            # preparing the csv row list by converting bytes class '' to string
            csv_str = uploaded_csv_file.readline().decode('utf-8')
            csv_list = csv_str.split(',')
            # strip() function executes over each item of csv_list(a list) to remove all the leading and trailing whitespaces
            csv_striped_list = [item.strip() for item in csv_list]
            csv_set = set(csv_striped_list)

            # retrieving the organisation name of the logged in user
            org_name = self.request.user.profile.organisation_name
            # retrieving the headers list for particular organisation
            model_header_list = Header.objects.filter(
                organisation_name=org_name).values_list('header', flat=True)
            header_set = set(model_header_list)

            if filename.endswith(settings.FILE_UPLOAD_TYPE):
                if uploaded_csv_file.size < int(settings.MAX_UPLOAD_SIZE):
                    if csv_set == header_set:
                        return uploaded_csv_file
                    else:
                        raise forms.ValidationError(
                            "Incorrect headers, please contact your administrator")
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

    Usage------
        1) 'registration.html' template: Generates the user form fields in the signup page for new users.
        2) 'update_profile.html' template: Generates the user form fields in the update profile page for existing users.
    """
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def save(self):  # pylint: disable = W0221
        user = super(UserForm, self).save(commit=False)
        password = self.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        return user


class ProfileForm(forms.ModelForm):
    """
    Modelform, generated from Django's Profile model.

    Usage------
        1) 'registration.html' template: Generates the profile form fields in the signup page for new users.
        2) 'update_profile.html' template: Generates the profile form fields in the update profile page for existing users.
    """
    class Meta:
        model = Profile
        fields = ('organisation_name', 'phone_number', 'profile_picture')
