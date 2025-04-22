from django.core import mail
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from livros.models import Usuario
from django.test import TestCase

class ConfirmacaoEmailTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nome='Erik',
            email='erik@example.com',
            senha='senha123'
        )
        self.usuario.set_senha('senha123')
        self.usuario.save()
        self.enviar_token_url = reverse('enviar_token')
        self.validar_token_url = reverse('validar_token')

    def test_enviar_token_sucesso(self):
        response = self.client.post(self.enviar_token_url, {'email': self.usuario.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.usuario.refresh_from_db()
        self.assertIsNotNone(self.usuario.token)
        self.assertTrue(self.usuario.token_expira_em > timezone.now())
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.usuario.token, mail.outbox[0].body)

    def test_enviar_token_usuario_nao_encontrado(self):
        response = self.client.post(self.enviar_token_url, {'email': 'naoexiste@example.com'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_validar_token_sucesso(self):
        self.usuario.gerar_novo_token()
        response = self.client.post(self.validar_token_url, {
            'email': self.usuario.email,
            'token': self.usuario.token
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.email_confirmado)

    def test_validar_token_invalido(self):
        self.usuario.gerar_novo_token()
        response = self.client.post(self.validar_token_url, {
            'email': self.usuario.email,
            'token': 'tokenerrado'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Token inválido', response.data['detail'])

    def test_validar_token_expirado(self):
        self.usuario.gerar_novo_token()
        self.usuario.token_expira_em = timezone.now() - timezone.timedelta(minutes=1)
        self.usuario.save()

        response = self.client.post(self.validar_token_url, {
            'email': self.usuario.email,
            'token': self.usuario.token
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Token expirado', response.data['detail'])
