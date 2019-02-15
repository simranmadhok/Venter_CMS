from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # ex: /venter/
    path('', TemplateView.as_view(template_name='Venter/home.html'), name='home'),
    # ex: /venter/home/
    path('home/', TemplateView.as_view(template_name='Venter/home.html'), name='home'),
    # ex: /venter/logout/
    path('logout/', views.user_logout, name='logout'),
    # ex: /venter/update_profile/5/
    path('update_profile/<int:pk>', views.UpdateProfileView.as_view(), name='update_profile'),
    # ex: /venter/register_employee/
    path('register_employee/', views.RegisterEmployeeView.as_view(), name='register_employee'),
    # ex: /venter/login/
    path('login/', auth_views.LoginView.as_view(template_name="Venter/login.html"), name='login'),
    # ex: /venter/upload_csv/
    path('upload_csv/', views.upload_csv_file, name='upload_csv'),
    # ex: /venter/download/
    path('download/', views.file_download, name='download_file'),
    # ex: /venter/category_list/civis/
    path('category_list/<organisation_name>', views.CategoryListView.as_view(), name='category_list'),
    # ex: /venter/dashboard_user/5/
    path('dashboard_user/<int:pk>', views.FilesByUserListView.as_view(), name='dashboard_user'),
    # ex: /venter/dashboard_staff/
    path('dashboard_staff/', views.FilesByOrganisationListView.as_view(), name='dashboard_staff'),
    # ex: /venter/contact_us/
    path('contact_us/', views.contact_us, name='contact_us'),
    path('predict/checkOutput/', views.handle_user_selected_data, name='checkOutput'),
]
