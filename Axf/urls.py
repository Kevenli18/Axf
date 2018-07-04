#! encoding: utf-8
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^axf/', include('app.urls', namespace='axf')),
]