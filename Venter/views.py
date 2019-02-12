import datetime
import os

from django import forms
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from Venter import upload_to_google_drive
from Venter.forms import CSVForm, ProfileForm, UserForm
from Venter.models import Category, File, Profile

from .manipulate_csv import EditCsv


def upload_csv_file(request):
    """
    View logic for uploading CSV file by a logged in user.

    For POST request-------
        1) The POST data, uploaded csv file and a request parameter are being sent to CSVForm as arguments
        2) If form.is_valid() returns true, the user is assigned to the uploaded_by field
        3) csv_form is saved and currently returns a simple httpresponse inplace of prediction results
    For GET request-------
        The csv_form is rendered in the template
    """
    if request.method == 'POST':
        csv_form = CSVForm(request.POST, request.FILES, request=request)
        if csv_form.is_valid():
            file_uploaded = csv_form.save(commit=False)
            file_uploaded.uploaded_by = request.user
            csv_form.save()
            if request.user.is_staff:
                return HttpResponseRedirect(reverse('dashboard_staff'))
            else:
                return HttpResponseRedirect(reverse('dashboard_user', args=(request.user.pk,)))
        else:
            return render(request, './Venter/upload_file.html', {'csv_form': csv_form})
    elif request.method == 'GET':
        csv_form = CSVForm(request=request)
        return render(request, './Venter/upload_file.html', {'csv_form': csv_form})

def handle_user_selected_data(request):
    """This function is used to handle the selected categories by the user"""
    if not request.user.is_authenticated:
        # Authentication security check
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        rows = request.session['Rows']
        correct_category = []
        company = request.session['company']
        if request.method == 'POST':
            file_name = request.session['filename']
            user_name = request.user.username
            for i in range(rows):
                # We are getting a list of values because the select tag was multiple select
                selected_category = request.POST.getlist(
                    'select_category' + str(i) + '[]')
                if request.POST['other_category' + str(i)]:
                    # To get a better picture of what we are getting try to print "request.POST.['other_category' + str(i)]", request.POST['other_category' + str(i)
                    # others_list=request.POST['other_category' + str(i)]
                    # for element in others_list:
                    #     print(element)
                    #     tuple = (selected_category,element)
                    tuple = (selected_category,
                             request.POST['other_category' + str(i)])
                    # print(request.POST['other_category' + str(i)])
                    # print(tuple)
                    # So here the correct_category will be needing a touple so the data will be like:
                    # [(selected_category1, selected_category2), (other_category1, other_category2)] This will be the output of the multi select
                    correct_category.append(tuple)
                else:
                    # So here the correct_category will be needing a touple so the data will be like:
                    # [(selected_category1, selected_category2)] This will be the output of the multi select
                    correct_category.append(selected_category)
        csv = EditCsv(file_name, user_name, company)
        csv.write_file(correct_category)
        if request.POST['radio'] != "no":
            # If the user want to send the file to Google Drive
            path_folder = request.user.username + "/CSV/output/"
            path_file = 'MEDIA/' + request.user.username + \
                "/CSV/output/" + request.session['filename']
            path_file_diff = 'MEDIA/' + request.user.username + "/CSV/output/Difference of " + request.session[
                'filename']
            upload_to_google_drive.upload_to_drive(path_folder,
                                                   'results of ' +
                                                   request.session['filename'],
                                                   "Difference of " +
                                                   request.session['filename'],
                                                   path_file,
                                                   path_file_diff)
    return redirect("/download")


def file_download(request):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        # Refer to the source: https://stackoverflow.com/questions/36392510/django-download-a-file/36394206
        path = os.path.join(settings.MEDIA_ROOT, request.user.username,
                            "CSV", "output", request.session['filename'])
        with open(path, 'rb') as csv:
            response = HttpResponse(
                csv.read())  # Try using HttpStream instead of this. This method will create problem with large numbers of rows like 25k+
            response['Content-Type'] = 'application/force-download'
            response['Content-Disposition'] = 'attachment;filename=results of ' + \
                request.session['filename']
        return response


def handle_uploaded_file(f, username, filename):
    """Just a precautionary step if signals.py doesn't work for any reason."""

    data_directory_root = settings.MEDIA_ROOT
    path = os.path.join(data_directory_root, username,
                        "CSV", "input", filename)
    path_input = os.path.join(data_directory_root, username, "CSV", "input")
    path_output = os.path.join(data_directory_root, username, "CSV", "output")

    if not os.path.exists(path_input):
        os.makedirs(path_input)

    if not os.path.exists(path_output):
        os.makedirs(path_output)

    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def user_logout(request):
    logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)


class CategoryListView(LoginRequiredMixin, ListView):
    """
    Arguments------
        1) ListView: View to display the category list for the organisation to which the logged in user belongs
        2) LoginRequiredMixin: Request to update profile details by non-authenticated users, will throw an HTTP 404 error

    Functions------
        1) get_queryset(): Returns a new QuerySet filtering categories based on the organisation name passed in the parameter.
    """
    model = Category

    def get_queryset(self):
        return Category.objects.filter(organisation_name=self.request.user.profile.organisation_name)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
    Arguments------
        1) UpdateView: View to update the user profile details for the logged-in user
        2) LoginRequiredMixin: Request to update profile details by non-authenticated users, will throw an HTTP 404 error
    """
    model = Profile
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return render(request, './Venter/update_profile.html', {'profile_form': profile_form})

    def get(self, request, *args, **kwargs):
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, './Venter/update_profile.html', {'profile_form': profile_form})


class RegisterEmployeeView(CreateView):
    """
    Arguments------
        1) CreateView: View to register a new user(employee) of an organisation.
    Note------
        The organisation name for a newly registered employee is taken from the profile information of the staff member registering the employee.
        The profile.save() returns an instance of Profile that has been saved to the database.
        This occurs only after the profile is created for a new user with the 'profile.user = user'
    """
    model = User

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            userObj = user_form.save()
            org_name = request.user.profile.organisation_name
            profile = Profile.objects.create(user=userObj, organisation_name=org_name)
            profile.save()
            return HttpResponseRedirect(reverse('dashboard_staff'))
        else:
            return HttpResponse("<h1>NO Profile created</h1>")

    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        return render(request, './Venter/registration.html', {'user_form': user_form})

class FilesByUserListView(generic.ListView):
    """
    Arguments------
        1) ListView: View to display the files uploaded by the logged-in user

    Functions------
        1) get_queryset(): Returns a new QuerySet filtering files uploaded by the logged-in user
    """
    model = File
    template_name = './Venter/dashboard_user.html'
    context_object_name = 'file_list'

    def get_queryset(self):
        return File.objects.filter(uploaded_by=self.request.user)

class FilesByOrganisationListView(generic.ListView):
    """
    Arguments------
        1) ListView: View to display the files uploaded by all the users of an organisation

    Functions------
        1) get_queryset(): Returns a new QuerySet filtering files uploaded by all the users of a particular organisation
    """
    model = File
    template_name = './Venter/dashboard_staff.html'
    context_object_name = 'file_list'

    def get_queryset(self):
        """
        This function performs the following tasks in sequence:
            1) get the organisation name of the logged-in satff member
            2) get the profile of all the users belonging to that organisation
            3) get the csv files of all those users in a list[]
        """
        org_name = self.request.user.profile.organisation_name
        org_profiles = Profile.objects.filter(organisation_name=org_name)
        files_list = []
        for x in org_profiles:
            files_list += File.objects.filter(uploaded_by=x.user)
        return files_list

def contact_us(request):
    """
    View logic to email the administrator the contact details submitted by an organisation.
    The contact details are submitted through the 'contact_us' template form.

    For POST request-------
        The contact details of an organisation are collected in the form.
        The email and phone number validation is performed.
        The formd details are packed together in the body of the email.
        An email is sent to the website administrator.
    For GET request-------
        The contact_us template is rendered
    """
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        contact_no = request.POST.get('contact_no')
        email = request.POST.get('email')
        requirement_details = request.POST.get('requirement_details')

        try:
            validate_email(email)
            # validate phone number
            # get current date and time
            now = datetime.datetime.now()
            print(now.strftime("%Y-%m-%d %H:%M"))
            date_time = now.strftime("%Y-%m-%d %H:%M")
            # prepare email_body
            email_body = "Dear Admin,\n\n Following are the inquiry details:\n\n Inquiry Date and Time: "+date_time+"\n Company Name: "+company_name+"\n Contact Number: "+contact_no+"\n Email address: "+email+"\n Requirement Details: "+requirement_details+"\n\n"
            print(email_body)
            # use send_mail() to submit form details to the administrator
            return HttpResponse('<h3>Details submitted</h3>')
        except forms.ValidationError:
            error_message = "Please enter a valid email address"
            return render(request, './Venter/contact_us.html', {
                'error_message': error_message})
    elif request.method == 'GET':
        return render(request, './Venter/contact_us.html')
