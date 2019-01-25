from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # ex: /venter/
    path('', TemplateView.as_view(template_name='Login/home.html'), name='home'),
    # ex: /venter/home/
    path('home/', TemplateView.as_view(template_name='Login/home.html'), name='home'),
    # ex: /venter/logout/
    path('logout/', views.user_logout, name='logout'),
    # ex: /venter/update_profile/5/
    path('update_profile/<int:pk>', views.UpdateProfileView.as_view(), name='update_profile'),
    # ex: /venter/create_profile/
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
    # ex: /venter/login/
    path('', include('django.contrib.auth.urls')),
    # ex: /venter/upload_csv/5/
    path('upload_csv/<int:pk>', views.upload_csv_file, name='upload_csv'),
    # ex: /venter/download/
    path('download/', views.file_download, name='download_file'),
    # ex: /venter/category_list/civis/
    path('category_list/<organisation_name>', views.CategoryListView.as_view(), name='category_list'),
    path('predict/checkOutput/', views.handle_user_selected_data, name='checkOutput'),
]

if settings.DEBUG:
    # ex: /media/Organisation/Organisation%20Logo/2018/12/08/logo1.png
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
