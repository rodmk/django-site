from django.contrib import admin

from apps.hello.models import Greeting, Response

# Register your models here.
admin.site.register(Greeting)
admin.site.register(Response)
