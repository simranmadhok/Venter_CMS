from django import forms
from django.contrib.auth.models import User

from Backend import settings
from Venter.models import File, Header, Profile


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
            # extracting and converting the header from bytes to string format
            csv_str = uploaded_csv_file.readline().decode('utf-8')

            # converting the headers from string to list using comma separated delimiters
            csv_list = csv_str.split(',')

            # strip() function executes over each item of csv_list to remove all the leading and trailing whitespaces
            # this should normalise all the header categories with whitespaces in them
            # then we cast the list to a set to allow us to validate it with the organisation's header list
            csv_striped_list = [item.strip() for item in csv_list]
            csv_set = set(csv_striped_list)

            # obtaining the organisation name of the logged in user
            # this retrieves the header list for a particular organisation and casts it to a set
            org_name = self.request.user.profile.organisation_name
            model_header_list = Header.objects.filter(
                organisation_name=org_name).values_list('header', flat=True)
            header_set = set(model_header_list)

            # validation of the filetype based on the extension type .csv
            # validation of the filesize based on the size limit 5MB
            # validation of the header list extracted from the csv file and the logged-in user's organisation
            filename = uploaded_csv_file.name
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

    Meta class------
        1) declares 'User' as the model class to generate the 'user_form'
        2) includes only five fields in the 'user_form' from the User model

    Usage------
        1) 'registration.html' template: Generates the user form fields in the signup page for new users
        2) 'update_profile.html' template: Generates the user form fields in the update profile page for existing users
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

    Meta class------
        1) declares 'Profile' as the model class to generate the 'profile_form'
        2) includes only three fields in the 'profile_form' from the Profile model

    Usage------
        1) 'registration.html' template: Generates the profile form fields in the signup page for new users
        2) 'update_profile.html' template: Generates the profile form fields in the update profile page for existing users
    """
    class Meta:
        model = Profile
        fields = ('organisation_name', 'phone_number', 'profile_picture')
