from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Fach, Thema, Karten
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, CreateThemaForm, CreateKartenForm
from slugify import slugify

from rest_framework import viewsets
from .serializers import KartenSerializer
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import serializers
# Create your class-based-views here.
class ThemenKartenViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cards to be viewed or edited.
    """
    queryset = Karten.objects.all()
    serializer_class = KartenSerializer
    http_method_names = ['get']

    def get_queryset(self):
        thema = self.kwargs.get("karten_thema")
        return Karten.objects.filter(karten_thema__link=thema)

class KartenViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cards to be viewed or edited.
    """
    queryset = Karten.objects.all()
    serializer_class = KartenSerializer
    http_method_names = ['get']
# Create your method-based-views here.
def vueMe(request):
    return render(request=request, 
                  template_name="main/index.html")


def homepage(request):
    neusteThemen = Thema.objects.all().order_by('-datum')[:3]

    return render(request=request, 
                  template_name="main/faecher.html",
                  context={"faecher": Fach.objects.all, "neusteThemen": neusteThemen})

@login_required(login_url='/login/')
def profilePage(request, userName):
    allMyThemen = Thema.objects.filter(author=request.user).order_by('-datum')
    aktUser = request.user

    return render(request=request, 
                  template_name="main/profile.html",
                  context={"allMyThemen": allMyThemen, "aktUser": aktUser, "slugName": userName})

@login_required(login_url='/login/')
def ThemaErstellen(request):
    if request.method == "POST":
        form = CreateThemaForm(request.POST)
        if form.is_valid():
            new_thema = Thema(name=form.cleaned_data.get("name"), 
                              inhalt=form.cleaned_data.get("inhalt"), 
                              thema_fach=form.cleaned_data.get("thema_fach"),
                              author=request.user,
                              link=slugify(form.cleaned_data.get("name")))               ## We use slugify here for valid link-slug
            new_thema.save()
            themen_name = form.cleaned_data.get("name")
            messages.success(request, "Ein neuer Beitrag wurde erstellt und wird geprueft: '{}'. Danke fuer die Bemuehungen :)".format(themen_name))
            return redirect('/profile/{}'.format(request.user))
    form = CreateThemaForm

    return render(request,
                  "main/ThemaErstellen.html",
                  context={"form":form})

@login_required(login_url='/login/')
def KartenErstellen(request):
    form = CreateKartenForm
    if request.method == "POST":
        form = CreateKartenForm(request.POST)
        if form.is_valid():
            new_karte = Karten(frage=form.cleaned_data.get("frage"), antwort=form.cleaned_data.get("antwort"), karten_thema=form.cleaned_data.get("karten_thema"), is_published="nein")
            new_karte.save()
            current_thema = form.cleaned_data.get("karten_thema")
            frage=form.cleaned_data.get("frage")
            messages.success(request, "Die Karte '{}' wurde zum Thema '{}' hinzugefügt. \n Danke!".format(frage, current_thema))

    return render(request,
                  "main/KartenErstellen.html",
                  context={"form":form})


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, "Neuer Account wurde erstellt: {}".format(username))
            login(request, user)
            messages.info(request, "Du bist nun eingeloggt als {}".format(username))
            return redirect("main:homepage")
        else:
            for msg in form.errors:
                messages.error(request, "{}".format(form.errors[msg]))
    form = NewUserForm

    return render(request,
                  "main/register.html",
                  context={"form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "Du bist nun ausgeloggt")

    return redirect("main:homepage")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "Du bist nun eingeloggt als {}".format(username))
                return redirect("main:homepage")
            else:
                messages.error(request, "Einlogdaten sind nicht richtig.")
        else:
                messages.error(request, "Einlogdaten sind nicht richtig.")
    form = AuthenticationForm()

    return render(request, "main/login.html", context={"form":form})


def erstes_stueck(request, erstes_stueck):
    faecher = [f.link for f in Fach.objects.all()]
    aktUser = request.user
    if erstes_stueck in faecher:
        gefundene_themen = Thema.objects.filter(thema_fach__link=erstes_stueck)
        kartenCount = []
        for t in gefundene_themen:
            gefundene_karten = Karten.objects.filter(karten_thema__link=t.link).exclude(is_published="nein")
            kartenCount.append(len(gefundene_karten))

        return render(request,
                      "main/themen.html",
                      {"themen": gefundene_themen, "kartenCount": kartenCount}
                      )


    themen = [t.link for t in Thema.objects.all()]
    if erstes_stueck in themen:
        gefundenes_thema = Thema.objects.filter(link=erstes_stueck)
        for t in gefundenes_thema:
            current_fach = t.thema_fach
        gefundene_themen = Thema.objects.filter(thema_fach__link=current_fach)
        gefundene_karten = Karten.objects.filter(karten_thema__link=erstes_stueck)
        return render(request,
                      "main/thema.html",
                      {"thema": gefundenes_thema, "themen": gefundene_themen, "KarteiK": gefundene_karten, "aktUser": aktUser, "curSlug": erstes_stueck},
                      )

    return render(request, "main/404.html",)


def karten(request, erstes_stueck):
    themen = [t.link for t in Thema.objects.all()]
    themen_all = Thema.objects.all()
    if erstes_stueck in themen:
        gefundene_karten = Karten.objects.filter(karten_thema__link=erstes_stueck)
        current_thema = Thema.objects.filter(link=erstes_stueck).first()

        return render(request,
                      "main/karten.html",
                      {"Kartei": gefundene_karten, "zurueck": erstes_stueck, "current_thema": current_thema},
                      ) 


def umgekehrt(request, erstes_stueck):
    themen = [t.link for t in Thema.objects.all()]
    themen_all = Thema.objects.all()
    if erstes_stueck in themen:
        gefundene_karten = Karten.objects.filter(karten_thema__link=erstes_stueck)
        current_thema = Thema.objects.filter(link=erstes_stueck).first()

        return render(request,
                      "main/kartenUmgekehrt.html",
                      {"Kartei": gefundene_karten, "zurueck": erstes_stueck, "current_thema": current_thema},
                      ) 

def edit_post(request, erstes_stueck):
    thema_obj = Thema.objects.get(link=erstes_stueck)
    if request.user == thema_obj.author:
        if request.method == "POST":
            form = CreateThemaForm(request.POST)
            if form.is_valid():
                thema_obj.thema_fach = form.cleaned_data.get("thema_fach")
                thema_obj.name = form.cleaned_data.get("name")
                thema_obj.inhalt = form.cleaned_data.get("inhalt")
                thema_obj.is_published = "nein" #zur Sicherheit noch einmal freigeben
                thema_obj.save()
                themen_name = form.cleaned_data.get("name")
                messages.success(request, "Beitrag wurde editiert".format(themen_name))

                return redirect('/{}'.format(erstes_stueck))
                
        form = CreateThemaForm(initial={
              'thema_fach': thema_obj.thema_fach,
              'name': thema_obj.name,
              'inhalt': thema_obj.inhalt,
              })

        return render(request,
                      "main/ThemaEditieren.html",
                      context={"form":form})
    else:
        neusteThemen = Thema.objects.all().order_by('-datum')[:3]

        return render(request=request, 
                      template_name="main/faecher.html",
                      context={"faecher": Fach.objects.all, "neusteThemen": neusteThemen})