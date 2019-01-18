"""
Author: Meet Shah, Shivam Sharma

This view will render a simple html form if the request is GET. If request is POST then will collect the
uploaded csv file and save it in appropriate user account.
"""

import os

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.edit import FormView, UpdateView, CreateView
from Venter import upload_to_google_drive
from Venter.models import Category, Profile
from django.urls import reverse_lazy
from .forms import UserForm, ProfileForm, CSVForm
from .manipulate_csv import EditCsv
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

def upload_csv_file(request, pk):
    if request.method == 'POST':
        csv_form = CSVForm(request.POST, request.FILES, instance=request.user)
        if csv_form.is_valid():
            # perform header validation --> refer to script.py
            # extract file size from csv file uploaded, and add it to the 'file_size' field of File model
            # then save the csv file instance
            csv_form.save()
            return HttpResponse("<h1>Your csv file was uploaded</h1>")
        else:
            return HttpResponse("<h1>Error uploading file</h1>")

    elif request.method == 'GET':
        csv_form = CSVForm()
        return render(request, './Venter/upload_file.html', {'csv_form': csv_form})    


# def upload_file(request):
#     """This method handles the file uploaded and send the content to the frontend"""
#     if not request.user.is_authenticated:
#         # If not authenticated, redirect to upload_file.html
#         return render(request, 'Venter/upload_file.html')
#     else:
#         # Get the group of the user
#         query_set = Profile.objects.filter(user=request.user)  #pylint: disable=E1101
#         query_set_size = query_set.count()
#         error_dict = {'error': "Please contact admin to add you in group"}
#         if query_set_size == 0:
#             # If the group is not assigned, display error message
#             return render(request, 'Venter/error_message.html', error_dict)
#         else:
#             # Saving the group as company. This will be used for getting different prediction lists and category lists for different companies
#             company = str(query_set.all()[0])
#             request.session['company'] = company

#         # This post method is from clicking on 'Submit' button while uploading the csv file
#         if request.method == 'POST':
#             # Getting the data after all the validations
#             form = upload_file_form(request.POST, request.FILES)
#             user_name = request.user.username
#             file_name = str(request.FILES['file'].name)
#             if form.is_valid():
#                 # Execute the prediction of data only if the form is valid
#                 handle_uploaded_file(request.FILES['file'], user_name,
#                                      file_name)  # This is a precautionary step to see whether the folders for each user has been made or not
#                 # Creating an object of the class which will be used to manipulate all the csv data
#                 csv = EditCsv(file_name, user_name, company)
#                 # Checking whether the headers of the file are in the same format as given in settings.ICMC_HEADERS or settings.SPEAKUP_HEADERS based on their groups
#                 header_flag, category_list = csv.check_csvfile_header()
#                 if header_flag:
#                     # If all the headers are matching in the csv file
#                     dict_list, rows = csv.read_file()  # Here we are getting a list of dictionary (structure is in EditCsv.py) in dict_list and the rows which is the rest of the material in the csv file
#                     context = {'dict_list': dict_list, 'category_list': category_list, 'rows': rows}
#                     request.session['Rows'] = rows
#                     request.session['filename'] = file_name
#                     return render(request, 'Venter/predict_categories.html',
#                                   context)  # Sending the data in the Frontend to display
#                 else:
#                     # If the header_flag is false, delete the Input file
#                     csv.delete()
#                     form = upload_file_form()  # Reinitialize the upload_file_form
#                     return render(request, 'Venter/upload_file.html',
#                                   {'form': form, 'Error': "Please submit CSV file with valid headers !!!"})
#         else:
#             # If the request is not POST, display the form to submit
#             form = upload_file_form()
#         return render(request, 'Venter/upload_file.html', {'form': upload_file_form()})


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
                selected_category = request.POST.getlist('select_category' + str(i) + '[]')
                if request.POST['other_category' + str(i)]:
                    # To get a better picture of what we are getting try to print "request.POST.['other_category' + str(i)]", request.POST['other_category' + str(i)
                    # others_list=request.POST['other_category' + str(i)]
                    # for element in others_list:
                    #     print(element)
                    #     tuple = (selected_category,element)
                    tuple = (selected_category, request.POST['other_category' + str(i)])
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
            path_file = 'MEDIA/' + request.user.username + "/CSV/output/" + request.session['filename']
            path_file_diff = 'MEDIA/' + request.user.username + "/CSV/output/Difference of " + request.session[
                'filename']
            upload_to_google_drive.upload_to_drive(path_folder,
                                                   'results of ' + request.session['filename'],
                                                   "Difference of " + request.session['filename'],
                                                   path_file,
                                                   path_file_diff)
    return redirect("/download")


def file_download(request):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        # Refer to the source: https://stackoverflow.com/questions/36392510/django-download-a-file/36394206
        path = os.path.join(settings.MEDIA_ROOT, request.user.username, "CSV", "output", request.session['filename'])
        with open(path, 'rb') as csv:
            response = HttpResponse(
                csv.read())  # Try using HttpStream instead of this. This method will create problem with large numbers of rows like 25k+
            response['Content-Type'] = 'application/force-download'
            response['Content-Disposition'] = 'attachment;filename=results of ' + request.session['filename']
        return response


def handle_uploaded_file(f, username, filename):
    """Just a precautionary step if signals.py doesn't work for any reason."""

    data_directory_root = settings.MEDIA_ROOT
    path = os.path.join(data_directory_root, username, "CSV", "input", filename)
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
    """
    Author: Meet Shah
    source implementing logout: https://www.youtube.com/watch?v=l8f-KFxw-xU source implementing file delete: https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder-in-python
    Diff between os.unlink() and os.remove() => https://stackoverflow.com/questions/42636018/python-difference-between-os-remove-and-os-unlink-and-which-one-to-use
    """
    logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)
        

class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    def get_queryset(self):
        return Category.objects.filter(organisation_name=self.request.user.profile.organisation_name) # pylint: disable = E1101

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    # slug_field = 'user_id'
    success_url = reverse_lazy('home')
    # form_class = ProfileForm
    # template_name = './Venter/update_profile.html'

    def post(self, request, pk):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            messages.error(request, 'Please correct the error below.')

    def get(self, request, pk):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, './Venter/update_profile.html', {'user_form': user_form, 'profile_form': profile_form})        

class CreateProfileView(CreateView):
    model = Profile

    def post(self, request):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid(): 
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect(reverse('home', args=[]))
        else:
            messages.warning(request, 'Something went wrong in Venter, please try again')
            return HttpResponse("<h1>NO Profile created</h1>")

    def get(self, request):
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(request, './Venter/registration.html', {'user_form': user_form, 'profile_form': profile_form})

    
