"""WebServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from server.views import home
from server.views import  register
from server.views import login
from server.views import upload
from django.conf.urls.static import static
from WebServer import settings
from server.views import getBanners
from server.api import deleteBanner
from server.api import updateBanner
from server.views import addGoodItem

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    url(r'^home/?$', home),
    url(r'^register/?$',register),
    url(r'^login/?$',login),
    url(r'^upload/?$',upload),
    url(r'^banner/?$',getBanners),
    url(r'^deletebanner/?$',deleteBanner),
    url(r'^updatebanner/?$',updateBanner),
    url(r'^addgood/?$',addGoodItem),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)