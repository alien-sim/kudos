from django.contrib import admin

from kudos.apps.kudo_app.models.user import User
from kudos.apps.kudo_app.models.organization import Organization


class AdminUser(admin.ModelAdmin):
    list_display = ("email", )  
    search_fields = ("email", "first_name", 'last_name')
    list_filter = ("is_active",)

admin.site.register(User, AdminUser)

class AdminOrganization(admin.ModelAdmin):
    list_display = ("name", )  
    search_fields = ("name", )

admin.site.register(Organization, AdminOrganization)
