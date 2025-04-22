from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Usuario

class AutenticacaoTests(APITestCase):

    def setUp(self):
        self.url_cadastro = reverse('cadastro')
        self.url_login = reverse('view')
        self.url_logout = reverse('logout')

        self.dados_usuario = {
            'nome': 'Teste',
            'email': 'teste@exemplo.com',
            'senha': 'senha123'
        }

    def test_cadastro_usuario_sucesso(self):
        response = self.client.post(self.url_cadastro, self.dados_usuario)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Usuario.objects.filter(email=self.dados_usuario['email']).exists())

    def test_cadastro_usuario_ja_existente(self):
        Usuario.objects.create(
            nome='Teste',
            email='teste@exemplo.com',
            senha='qualquercoisa',
            is_logged=False
        )
        response = self.client.post(self.url_cadastro, self.dados_usuario)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cadastro_sem_email(self):
        dados = {
            'nome': 'Teste',
            'senha': 'senha123'
        }
        response = self.client.post(self.url_cadastro, dados)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_sucesso(self):
        self.client.post(self.url_cadastro, self.dados_usuario)
        response = self.client.post(self.url_login, {
            'email': 'teste@exemplo.com',
            'senha': 'senha123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.dados_usuario['email'])

    def test_login_credenciais_erradas(self):
        response = self.client.post(self.url_login, {
            'email': 'naoexiste@exemplo.com',
            'senha': 'errada'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_campos_vazios(self):
        dados = {
            'email': '',
            'senha': ''
        }
        response = self.client.post(self.url_login, dados)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_senha_incorreta(self):
        Usuario.objects.create(
            nome='Teste',
            email='teste@exemplo.com',
            senha='senha123'
        )
        dados = {
            'email': 'teste@exemplo.com',
            'senha': 'senhaalgoerrado'
        }
        response = self.client.post(self.url_login, dados)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_sem_email(self):
        dados = {
            'senha': 'senha123'
        }
        response = self.client.post(self.url_login, dados)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_sem_senha(self):
        dados = {
            'email': 'teste@exemplo.com'
        }
        response = self.client.post(self.url_login, dados)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_com_email_valido(self):
        self.client.post(self.url_cadastro, self.dados_usuario)
        self.client.post(self.url_login, {
            'email': self.dados_usuario['email'],
            'senha': self.dados_usuario['senha']
        })
        response = self.client.post(self.url_logout, {'email': self.dados_usuario['email']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Logout realizado com sucesso!')

    def test_logout_com_email_invalido(self):
        response = self.client.post(self.url_logout, {'email': 'inexistente@email.com'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Usuário não encontrado.')

    def test_logout_usuario_ja_deslogado(self):
        self.client.post(self.url_cadastro, self.dados_usuario)
        self.client.post(self.url_login, {
            'email': self.dados_usuario['email'],
            'senha': self.dados_usuario['senha']
        })
        self.client.post(self.url_logout, {'email': self.dados_usuario['email']})
        response = self.client.post(self.url_logout, {'email': self.dados_usuario['email']})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Usuário já está deslogado.')

    def test_logout_desativa_is_logged(self):
        self.client.post(self.url_cadastro, self.dados_usuario)
        self.client.post(self.url_login, {
            'email': self.dados_usuario['email'],
            'senha': self.dados_usuario['senha']
        })
        self.client.post(self.url_logout, {'email': self.dados_usuario['email']})
        
        usuario = Usuario.objects.get(email=self.dados_usuario['email'])
        self.assertFalse(usuario.is_logged)
