from django.contrib import admin
from django.urls import include, path
from pybo import views

app_name = "pybo"

## http://127.0.0.1:8000/pybo/5/
urlpatterns = [
    path("", views.index, name="index"),
    # http://127.0.0.1:8000/pybo/<int:question_id>/
    path("<int:question_id>/", views.detail, name="detail"),  #  dev_3
]
