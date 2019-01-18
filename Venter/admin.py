# Register your models here.
from django.contrib import admin
from Venter.models import Header, Category, File, Organisation, Profile
 
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
    verbose_name_plural = 'Employee Details'
    list_display=('organisation_name', 'phone_number', 'user')

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['username', 'first_name','last_name'] 
#     search_fields = ('username',)   

class OrganisationAdmin(admin.ModelAdmin):
    verbose_name_plural = 'Organisation Details'


admin.site.register(Header, HeaderAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Organisation, OrganisationAdmin)



