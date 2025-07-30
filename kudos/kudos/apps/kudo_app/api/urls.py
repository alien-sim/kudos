from django.urls import path

from kudos.apps.kudo_app.api.views.login import ViewAPILogin
from kudos.apps.kudo_app.api.views.user_profile import ViewAPIUserProfile


urlpatterns = [
    path(
        'login/', 
        ViewAPILogin.as_view(),
        name='login' 
    ),
    path(
        'user-profile/', 
        ViewAPIUserProfile.as_view(),
        name='user-profile' 
    )
]