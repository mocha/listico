from django.contrib import admin
from django.contrib.auth.models import User
from user_creation.forms import EmailAccountCreationForm
from email_login.useradmin import EmailLoginAdmin


class MyUserAdmin(EmailLoginAdmin):
    add_form = EmailAccountCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'email_user')}
        ),
    )

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)