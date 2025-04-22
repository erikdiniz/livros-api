from django.test import TestCase
from django.urls import reverse
from livros.models import Usuario
from django.contrib.auth.hashers import check_password

class UsuarioTestCase(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nome='Usuário Teste',
            email='teste@example.com',
            is_logged=True
        )
        self.usuario.set_senha('senha123')
        self.usuario.save()

    def test_editar_perfil_usuario(self):
        url = reverse('editar_usuario', kwargs={'email': self.usuario.email})
        dados = {
            'nome': 'Novo Nome',
            'email': 'novonome@example.com'
        }
        response = self.client.put(url, dados, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nome, 'Novo Nome')
        self.assertEqual(self.usuario.email, 'novonome@example.com')

    def test_trocar_senha_com_sucesso(self):
        url = reverse('alterar_senha', kwargs={'email': self.usuario.email})
        dados = {
            'senha_atual': 'senha123',
            'nova_senha': 'novaSenha456'
        }
        response = self.client.put(url, dados, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.usuario.refresh_from_db()
        self.assertTrue(check_password('novaSenha456', self.usuario.senha))

    def test_trocar_senha_com_senha_incorreta(self):
        url = reverse('alterar_senha', kwargs={'email': self.usuario.email})
        dados = {
            'senha_atual': 'senhaErrada',
            'nova_senha': 'novaSenha456'
        }
        response = self.client.put(url, dados, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Senha atual incorreta.', response.data['detail'])
