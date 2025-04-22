from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='view'),
    path('logout/', views.logout, name='logout'),
    path('livros/<str:email>/', views.livros_lista, name='livros'),
    path('usuario/<str:email>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuario/<str:email>/alterar-senha/', views.alterar_senha, name='alterar_senha'),
    path('usuario/enviar-token/', views.enviar_token, name='enviar_token'),
    path('usuario/validar-token/', views.validar_token, name='validar_token')
]