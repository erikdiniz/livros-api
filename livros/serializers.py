from rest_framework import serializers
from .models import Usuario, Livro

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nome', 'email']


class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = ['titulo', 'ano']