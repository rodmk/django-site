from django.urls import path

from apps.hello import views

urlpatterns = [
    path("", views.hello_world, name="hello_world"),
    path("create/", views.create_greeting, name="create_greeting"),
    path("list/", views.list_greetings, name="list_greetings"),
    path("greeting/<int:greeting_id>/", views.greeting_detail, name="greeting_detail"),
    path("greeting/<int:greeting_id>/reply/", views.add_response, name="add_response"),
]
