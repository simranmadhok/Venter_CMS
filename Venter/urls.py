from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name='Login/home.html'), name='home'),
    path('home/', TemplateView.as_view(template_name='Login/home.html'), name='home'),
    path('logout/', views.user_logout, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('', include('django.contrib.auth.urls')),

    path('predict/', views.upload_file, name='predict'),
    path('download/', views.file_download, name='download_file'),
    path('McgmCategory/', TemplateView.as_view(template_name='Venter/mcgm_categories.html'), name='McgmCategory'),
    path('SpeakupCategory/', TemplateView.as_view(template_name='Venter/speakup_categories.html'),
         name='SpeakupCategory'),
    path('predict/checkOutput/', views.handle_user_selected_data, name='checkOutput'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
