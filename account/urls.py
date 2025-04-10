from django.urls import path

from .views import (RegistrationView, ActivateView, CheckEmailView,
                    DeleteAccountView)

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('check-email/', CheckEmailView.as_view(), name="check_email"),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
]
