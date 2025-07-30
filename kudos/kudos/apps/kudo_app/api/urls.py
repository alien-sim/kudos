from django.urls import path

from kudos.apps.kudo_app.api.views.login import ViewAPILogin
from kudos.apps.kudo_app.api.views.user_profile import ViewAPIUserProfile
from kudos.apps.kudo_app.api.views.register import ViewAPIRegister
from kudos.apps.kudo_app.api.views.organization import ViewAPIOrganization


urlpatterns = [
    path(
        'login/', 
        ViewAPILogin.as_view(),
        name='login' 
    ),
    path(
        'register/', 
        ViewAPIRegister.as_view(),
        name='register' 
    ),
    path(
        'user-profile/', 
        ViewAPIUserProfile.as_view(),
        name='user-profile' 
    ),
    path(
        'organizations/', 
        ViewAPIOrganization.as_view(),
        name='organizations' 
    )
]