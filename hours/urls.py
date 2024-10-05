from django.urls import path

from . import views

urlpatterns = [
    path("", views.HoursIndexView.as_view(), name="hours_list"),
    path("add/", views.HoursCreateView.as_view(), name="hours_create"),
    path("edit/<int:pk>/", views.HoursUpdateView.as_view(), name="hours_update"),
    path("delete/<int:pk>/", views.HoursDeleteView.as_view(), name="hours_delete"),
    path("set_lang/", views.SetLangView.as_view(), name="set_lang"),
]
