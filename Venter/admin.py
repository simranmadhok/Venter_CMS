# Register your models here.
from django.contrib import admin
from Venter.models import Header, Category, File, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
 
class HeaderAdmin(admin.ModelAdmin):
    list_display = ('organisation_name', 'header')
    list_filter = ['organisation_name']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('organisation_name', 'category')    
    list_filter = ['organisation_name']

class FileAdmin(admin.ModelAdmin):
    list_display=('file_name', 'uploaded_by', 'uploaded_date') 
    list_filter = ['uploaded_date']   

class ProfileAdmin(admin.ModelAdmin):
    verbose_name_plural = 'Organisation Details'
    fk_name = 'user'
    #readonly_fields=['organisation_name']
    list_display=('organisation_name', 'phone_number')


admin.site.register(Header, HeaderAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Profile, ProfileAdmin)
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)



