"""FelixWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from felix_web import views as web
from django.contrib.auth.views import auth_login, auth_logout

urlpatterns = [
    url('^$', web.HomeView.as_view(), name='Home'),
    url(r"^account/", include("account.urls")),
    url(r"^sessions/", web.SessionKoView.as_view(), name='SessionsKO'),
    url(r"^session_detail/", web.SessionKoDetail.as_view(), name='SessionDetail'),
    url(r"^save_turn/?$", web.SaveTurn.as_view(), name='SaveTurn'),
    path('admin/', admin.site.urls),
]
