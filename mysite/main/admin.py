from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Fach, Thema, Karten
from tinymce.widgets import TinyMCE
from django.db import models
from django.utils.html import format_html
from django.urls import reverse
# Register your models here.


class ThemaAdmin(admin.ModelAdmin):
    #    fields = ["name",              ## hier Reihenfolge
    #              "datum",
    #              "inhalt",
    #              ]
    fieldsets = [  # hier mit Ueberschriften
        ("Veröffentlicht", {"fields": ["is_published"]}),
        ("Klausurthema?", {"fields": ["is_klausur"]}),
        ("Thema/Erstelldatum", {"fields": ["name", "datum"]}),
        ("Link", {"fields": ["link"]}),
        ("Fach", {"fields": ["thema_fach"]}),
        ("Style", {"fields": ["style"]}),
        ("Inhalt", {"fields": ["inhalt", "goto_button"]}),
        ("Author", {"fields": ["author"]}),
    ]
    readonly_fields = ('goto_button', )

    # formfield_overrides = {
    #     models.TextField: {'widget': TinyMCE(
    #         mce_attrs={'valid_elements': '*[*]'},
    #     )}
    # }

    list_display = (
        'name',
        'goto_button',
        'datum',
    )

    def goto_button(self, obj):
        return format_html('<a class="button" href="{}">goto</a>&nbsp;',
                           reverse('main:erstes_stueck', args=[obj.link]),)
    goto_button.allow_tags = True


def make_published(modeladmin, request, queryset):
    queryset.update(is_published='ja')


make_published.short_description = "veröffentliche alle ausgewälten Elemente"


def make_notpublished(modeladmin, request, queryset):
    queryset.update(is_published='nein')


make_notpublished.short_description = "verstecke alle ausgewälten Elemente"


class KartenAdmin(admin.ModelAdmin):
    list_display = ['frage', 'antwort', 'karten_thema', 'is_published']
    #ordering = ['frage', 'is_published', 'antwort']
    actions = [make_published, make_notpublished]


admin.site.register(Fach)
admin.site.register(Karten, KartenAdmin)

admin.site.register(Thema, ThemaAdmin)
