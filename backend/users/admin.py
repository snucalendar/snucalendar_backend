from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import CalendarUser

# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', )}),
        ('Permissons', {'fields': ('is_admin',)})
    )

    add_fieldsets = (None, {
        'classes': ('wide',),
        'fields': ('email', 'password', 'username',)
    })

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(CalendarUser, UserAdmin)
admin.site.unregister(Group)