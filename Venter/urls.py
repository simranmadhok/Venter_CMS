from django.urls import path, include
from . import views # pylint: disable = E0611
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name='Login/home.html'), name='home'),
    path('home/', TemplateView.as_view(template_name='Login/home.html'), name='home'),
    path('logout/', views.user_logout, name='logout'),
    path('updateProfile/<int:pk>', views.UpdateProfileView.as_view(), name='update_profile'),
    path('createProfile/', views.CreateProfileView.as_view(), name='create_profile'),
    path('', include('django.contrib.auth.urls')),

    # path('predict/', views.upload_file, name='predict'),
    path('uploadCsv/<int:pk>', views.upload_csv_file, name='upload_csv'),
    path('download/', views.file_download, name='download_file'),
    path('categoryList/<organisation_name>', views.CategoryListView.as_view(), name='category_list'),
    path('predict/checkOutput/', views.handle_user_selected_data, name='checkOutput'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
