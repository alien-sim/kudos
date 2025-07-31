from django.contrib import admin

from kudos.apps.kudo_app.models.user import User
from kudos.apps.kudo_app.models.organization import Organization
from kudos.apps.kudo_app.models.kudo import Kudo
from kudos.apps.kudo_app.models.kudo_tracker import WeeklyKudoTracker


class AdminUser(admin.ModelAdmin):
    list_display = ("email", )  
    search_fields = ("email", "first_name", 'last_name')
    list_filter = ("is_active",)

admin.site.register(User, AdminUser)

class AdminOrganization(admin.ModelAdmin):
    list_display = ("name", )  
    search_fields = ("name", )

admin.site.register(Organization, AdminOrganization)

class AdminKudo(admin.ModelAdmin):
    list_display = ("sender", 'receiver' )  
    search_fields = ("name", )

admin.site.register(Kudo, AdminKudo)

class AdminWeeklyKudoTracker(admin.ModelAdmin):
    list_display = ("user", 'kudos_given', 'week_start' )  
    search_fields = ("user__email", )

admin.site.register(WeeklyKudoTracker, AdminWeeklyKudoTracker)
