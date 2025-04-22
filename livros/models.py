from uuid import uuid4
import uuid
from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta

class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=128)
    is_logged = models.BooleanField(default=False)
    imagem = models.ImageField(default='default.png')
    email_confirmado = models.BooleanField(default=False)
    token = models.CharField(max_length=64, blank=True, null=True)
    token_expira_em = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Username: {self.nome} | Email: {self.email}'
    
    def set_is_logged(self, status):
        self.is_logged = status
        self.save()
    
    def set_senha(self, nova_senha):
        self.senha = make_password(nova_senha)
        self.save()

    def set_confirmado(self, status=True):
        self.email_confirmado = status
        self.save()

    def gerar_novo_token(self):
        self.token = str(uuid.uuid4())
        self.token_expira_em = timezone.now() + timedelta(minutes=15)
        self.save()
    
class Livro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    titulo = models.CharField(max_length=100, default='')
    ano = models.IntegerField()
    validado = models.BooleanField(default=False)


    def __str__(self):
        return f'Título: {self.titulo} | Ano: {self.ano}'
