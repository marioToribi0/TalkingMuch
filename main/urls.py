from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("forms/", views.forms, name="forms"),
    path("upload/", views.upload, name="upload"),
    path("results/", views.results, name="results"),
    path("file_results/",views.file_result, name="file_result")
]
