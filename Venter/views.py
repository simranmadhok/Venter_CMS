import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from Venter import upload_to_google_drive
from Venter.models import Category, Profile

from Venter.forms import CSVForm, ProfileForm, UserForm
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
            return HttpResponse("<h1>Your csv file was uploaded, redirect user to prediction page (pie charts, tables..)</h1>")
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
        1) UpdateView: View to update the user profile details for the logged in user
        2) LoginRequiredMixin: Request to update profile details by non-authenticated users, will throw an HTTP 404 error
    """
    model = Profile
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid(): # pylint: disable = R1705
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            messages.error(request, 'Please correct the error below.')

    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, './Venter/update_profile.html', {'user_form': user_form, 'profile_form': profile_form})


class CreateProfileView(CreateView):
    """
    Arguments------
        1) CreateView: View to create the user profile for a new user.
    Note------
        profile_form.save(commit=False) returns an instance of Profile that hasn't yet been saved to the database.
        The profile.save() returns an instance of Profile that has been saved to the database.
        This occurs only after the profile is created for a new user with the 'profile.user = user'
    """
    model = Profile

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect(reverse('home', args=[]))
        else:
            messages.warning(
                request, 'Something went wrong in Venter, please try again')
            return HttpResponse("<h1>NO Profile created</h1>")

    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request, './Venter/registration.html', {'user_form': user_form, 'profile_form': profile_form})
