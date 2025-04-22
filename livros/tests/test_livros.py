from django.test import TestCase
from django.urls import reverse
from livros.models import Usuario, Livro
from rest_framework import status


class Livros(TestCase):
    def setUp(self):
        # Criação de um usuário e livros para testar
        self.usuario = Usuario.objects.create(
            nome='Test User',
            email='testuser@example.com',
            senha='password123',
            is_logged=True  # Defina o is_logged como True para simular um usuário autenticado
        )
        self.usuario.set_senha('password123')  # Define a senha com o método do modelo
        self.usuario.save()

        # Criação de livros
        self.livro1 = Livro.objects.create(titulo='Livro 1', ano=2000)
        self.livro2 = Livro.objects.create(titulo='Livro 2', ano=2010)
        self.livro3 = Livro.objects.create(titulo='Outro Livro', ano=2020)

        # URL para a listagem de livros, passando o email corretamente
        self.url = reverse('livros', kwargs={'email': self.usuario.email})

    def test_listagem_com_filtro(self):
        response = self.client.get(self.url, {'ano_min': 2005})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_listagem_paginada(self):
        response = self.client.get(self.url, {'page_size': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], 3)

    def test_listagem_com_busca(self):
        response = self.client.get(self.url, {'search': 'Outro'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_listagem_ordenada_por_ano_descendente(self):
        response = self.client.get(self.url, {'order_by': '-ano'})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data['results']), 0)
        self.assertEqual(response.data['results'][0]['ano'], 2020)

    def test_listagem_ordenada_por_titulo(self):
        response = self.client.get(self.url, {'order_by': 'titulo'})
        self.assertEqual(response.status_code, 200)

        results = response.data.get('results', [])
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]['ano'], 2000)