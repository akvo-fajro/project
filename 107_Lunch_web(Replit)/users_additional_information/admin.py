from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserAdditionalInformation

# Register your models here.
class UserAdditionalInformationInline(admin.StackedInline):
    model = UserAdditionalInformation
    can_delete = False
    verbose_name_plural = 'useradditionalinformation'


class UserAdmin(BaseUserAdmin):
    inlines = (UserAdditionalInformationInline,)


admin.site.unregister(User)
admin.site.register(User,UserAdmin)