from rest_framework import serializers
from .models import Karten, Thema

class KartenSerializer(serializers.ModelSerializer):

    karten_thema = serializers.CharField(source='karten_thema.link')

    class Meta:
        model = Karten
        fields = ['id', 'karten_thema', 'frage', 'antwort']