from django.urls import path

from kudos.apps.kudo_app.api.views.login import ViewAPILogin


urlpatterns = [
    path(
        'login/', 
        ViewAPILogin.as_view(),
        name='login' 
    )
]