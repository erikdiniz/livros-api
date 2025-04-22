from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
from django.forms import ValidationError
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Usuario, Livro
from .serializers import UsuarioSerializer, LivroSerializer
from rest_framework.pagination import PageNumberPagination

@api_view(['POST'])
def cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    imagem = request.FILES.get('imagem')

    if not nome or not email or not senha:
        return Response({'detail': 'Nome, email e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

    usuario = Usuario.objects.filter(email=email).first()

    if usuario:
        return Response({'detail': 'Email já cadastrado.'}, status=status.HTTP_400_BAD_REQUEST)
    
    usuario = Usuario.objects.create(
        nome = nome,
        email = email,
        senha = make_password(senha),
        is_logged = False,
        imagem = imagem
    )
    
    usuario.save()
    
    return Response(UsuarioSerializer(usuario).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    usuario = Usuario.objects.filter(email=email).first()

    if not usuario or not check_password(senha, usuario.senha):
        return Response({'detail': 'Email ou senha incorretos.'}, status=status.HTTP_401_UNAUTHORIZED)

    if usuario.is_logged:
            return Response({'detail': 'Usuário já está autenticado.'}, status=status.HTTP_400_BAD_REQUEST)

    if usuario and check_password(senha, usuario.senha):
        usuario.set_is_logged(True)
        usuario.save()
        return Response({'detail': 'Login realizado com sucesso!', 'email': usuario.email}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def logout(request):
    email = request.POST.get('email')

    usuario = Usuario.objects.filter(email=email).first()

    if not usuario:
        return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    if not usuario.is_logged:
        return Response({'detail': 'Usuário já está deslogado.'}, status=status.HTTP_400_BAD_REQUEST)

    usuario.set_is_logged(False)
    usuario.save()

    return Response({'detail': 'Logout realizado com sucesso!'}, status=status.HTTP_200_OK)

def get_livros_filtrados(request, usuario=None):
    queryset = Livro.objects.all()

    if not usuario or not usuario.email_confirmado:
        queryset = queryset.filter(validado=False)

    ano_min = request.query_params.get('ano_min')
    if ano_min:
        try:
            queryset = queryset.filter(ano__gte=int(ano_min))
        except ValueError:
            raise ValidationError({'detail': 'ano_min deve ser um número inteiro.'})

    ano_max = request.query_params.get('ano_max')
    if ano_max:
        try:
            queryset = queryset.filter(ano__lte=int(ano_max))
        except ValueError:
            raise ValidationError({'detail': 'ano_max deve ser um número inteiro.'})

    order_by = request.query_params.get('order_by')
    opcoes_validas = ['titulo', 'ano', '-titulo', '-ano']
    if order_by:
        if order_by in opcoes_validas:
            queryset = queryset.order_by(order_by)
        else:
            raise ValidationError({'detail': f"Parâmetro 'order_by' inválido. Use: {opcoes_validas}"})

    search = request.query_params.get('search')
    if search:
        queryset = queryset.filter(titulo__icontains=search)

    return queryset

@api_view(['GET'])
def livros_lista(request, email):
    usuario = Usuario.objects.filter(email=email).first()

    if not usuario:
        return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    if not usuario.is_logged:
        return Response({'detail': 'Usuário não está autenticado.'}, status=status.HTTP_400_BAD_REQUEST)

    livros_qs = get_livros_filtrados(request, usuario)

    paginator = PageNumberPagination()
    paginator.page_size = int(request.query_params.get('page_size', 10))
    paginated_qs = paginator.paginate_queryset(livros_qs, request)

    serializer = LivroSerializer(paginated_qs, many=True)

    return paginator.get_paginated_response(serializer.data)

@api_view(['PUT'])
def editar_usuario(request, email):
    usuario = Usuario.objects.filter(email=email).first()

    if not usuario:
        return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    if not usuario.is_logged:
        return Response({'detail': 'Usuário não está autenticado.'}, status=status.HTTP_401_UNAUTHORIZED)

    nome = request.data.get('nome')
    novo_email = request.data.get('email')
    imagem = request.FILES.get('imagem')  

    if nome:
        usuario.nome = nome

    if novo_email:
        usuario.email = novo_email

    if imagem:
        usuario.imagem = imagem

    usuario.save()
    return Response({'detail': 'Cadastro atualizado com sucesso.'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def alterar_senha(request, email):
    usuario = Usuario.objects.filter(email=email).first()

    if not usuario:
        return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    if not usuario.is_logged:
        return Response({'detail': 'Usuário não está autenticado.'}, status=status.HTTP_401_UNAUTHORIZED)

    senha_atual = request.data.get('senha_atual')
    nova_senha = request.data.get('nova_senha')

    if not senha_atual or not nova_senha:
        return Response({'detail': 'Preencha os campos de senha atual e nova senha.'}, status=status.HTTP_400_BAD_REQUEST)

    if not check_password(senha_atual, usuario.senha):
        return Response({'detail': 'Senha atual incorreta.'}, status=status.HTTP_400_BAD_REQUEST)

    usuario.set_senha(nova_senha)
    usuario.save()

    return Response({'detail': 'Senha alterada com sucesso.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def enviar_token(request):
    email = request.POST.get('email')
    usuario = Usuario.objects.filter(email=email).first()

    if not usuario:
        return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    usuario.gerar_novo_token()

    send_mail(
        subject='Seu token de verificação',
        message=f'Seu token é: {usuario.token}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[usuario.email],
        fail_silently=False,
    )

    return Response({'detail': 'Token enviado para o e-mail.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def validar_token(request):
    email = request.POST.get('email')
    token = request.POST.get('token')

    usuario = Usuario.objects.filter(email=email).first()

    if not usuario:
        return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    if usuario.token != token:
        return Response({'detail': 'Token inválido.'}, status=status.HTTP_400_BAD_REQUEST)

    if timezone.now() > usuario.token_expira_em:
        return Response({'detail': 'Token expirado.'}, status=status.HTTP_400_BAD_REQUEST)

    usuario.set_confirmado()
    usuario.save()
    return Response({'detail': 'Token válido!'}, status=status.HTTP_200_OK)
