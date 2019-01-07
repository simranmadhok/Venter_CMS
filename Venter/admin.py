# Register your models here.
from django.contrib import admin
from Venter.models import Organisation, Header, Category, File
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
 
# class OrganisationInline(admin.StackedInline):
#     model = Organisation
#     can_delete = False
#     verbose_name_plural = 'Organisation'
#     fk_name = 'user'

# class UserAdmin(BaseUserAdmin):
#     inlines = (OrganisationInline,)


admin.site.register(Header)
admin.site.register(Category)
admin.site.register(File)
admin.site.register(Organisation)
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)


