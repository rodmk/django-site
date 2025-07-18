from django.urls import path

from apps.hello import views

urlpatterns = [
    path("", views.hello_world, name="hello_world"),
]
