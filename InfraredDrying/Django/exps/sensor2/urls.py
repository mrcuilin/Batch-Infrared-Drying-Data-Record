"""TunnelDrying URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from . import views
from django.contrib import admin

urlpatterns = [
    url(r'RUN$', views.commandRun, name='RUN'),
    url(r'STOP$', views.commandStop, name='STOP'),
    url(r'DAYS*$', views.dayList, name='DAYS'),
    url(r'YEARS$', views.yearList, name='YEARS'),
    url(r'SESSIONS*$', views.sessionList, name='SESSIONS'),
    url(r'DOWNLOAD*$', views.download, name='DOWNLOAD'),
    url(r'SHOW*$', views.show, name='SHOW'),
    url(r'SHOWRAW*$', views.showRaw, name='SHOWRAW'),
    url(r'SHOWGRAPH*$', views.showGraph, name='SHOWGRAPH'),
    url(r'STATUS$', views.result, name='STATUS'),
    url(r'^$', views.result, name='result'),
]

