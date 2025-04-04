"""
URL configuration for dawn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from hours.views import HoursIndexView, ProfileUpdateView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    # use explicit paths for login and logout for the overridden views
    path('', include('account.urls')),
    path('hours/', include('hours.urls')),
    path('admin/', admin.site.urls),
    path('impersonate/', include('impersonate.urls')),
    path('', HoursIndexView.as_view(), name="hours_list"),
    path('profile/<int:pk>', ProfileUpdateView.as_view(), name="profile"),
    path('__reload__/', include('django_browser_reload.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
