"""mysite URL Configuration

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
from django.urls import include, path
from rest_framework import routers
from . import views

app_name = "main"

router = routers.DefaultRouter()
router.register(r'karten', views.KartenViewSet, base_name='karten_thema.name')

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("erstellen/", views.ThemaErstellen, name="ThemaErstellen"),
    path("karten-erstellen/", views.KartenErstellen, name="KartenErstellen"),
    path("profile/<userName>", views.profilePage, name="profilePage"),
    path("vue/", views.vueMe, name="vueMe"),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('test/<karten_thema>', views.ThemenKartenViewSet.as_view({'get': 'list'}), name='kartenThemen'),
    # has to be in the end because it also serves as 404
    path("<erstes_stueck>", views.erstes_stueck, name="erstes_stueck"),
    path("<erstes_stueck>/edit", views.edit_post, name="edit_post"),
    path("<erstes_stueck>/karten", views.karten, name="karten"),
    path("<erstes_stueck>/umgekehrt", views.umgekehrt, name="umgekehrt"),
]
