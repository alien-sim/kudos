from django.contrib import admin

from kudos.apps.kudos.models.user import User


class AdminUser(admin.ModelAdmin):
    list_display = ("email", )  
    search_fields = ("email", "first_name", 'last_name')
    list_filter = ("is_active",)

admin.site.register(User, AdminUser)
