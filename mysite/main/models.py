from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.

class Fach(models.Model):
    name = models.CharField(max_length=10)
    beschreibung = models.CharField(max_length=200)
    link = models.CharField(max_length=10, default=1)

    class Meta:
        verbose_name_plural = "Fächer"

    def __str__(self):
        return self.name

class Thema(models.Model):
    name = models.CharField(max_length=200)
    inhalt = models.TextField()
    datum = models.DateTimeField("Erstelldatum", default=timezone.now)
    style = models.CharField(max_length=200, default="", blank=True)

    thema_fach = models.ForeignKey(Fach, default=1, verbose_name="dasfach", on_delete=models.SET_DEFAULT)
    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT)
    link = models.CharField(max_length=200, default=1)
    is_published = models.CharField(max_length=20, default="nein")
    def __str__(self):
        return self.name

class Karten(models.Model):
    frage = models.CharField(max_length=200)
    antwort = models.CharField(max_length=200)
    karten_thema = models.ForeignKey(Thema, default=1, verbose_name="Thema", on_delete=models.SET_DEFAULT)
    is_published = models.CharField(max_length=20, default="ja")
    #link = models.CharField(max_length=200, default=1)
    
    class Meta:
        verbose_name_plural = "Karten"

    def __str__(self):
        return self.frage