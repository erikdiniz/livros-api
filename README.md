# 📚 API - Lista de livros

Uma API desenvolvida em Django e Django REST Framework para gerenciamento de usuários e listagem de livros.

💡 As funcionalidades descritas abaixo podem ser testadas via ferramentas como o [Postman](https://www.postman.com/) utilizando os endpoints fornecidos.

## 🚀 Funcionalidades Principais

### 👤 Autenticação e Usuários
- Cadastro de novos usuários
   - Endpoint: POST /cadastro/
   - Parâmetros (form-data):
      - nome (string) – obrigatório
      - email (string) – obrigatório
      - senha (string) – obrigatório
      - imagem (file) – opcional

- Login
   - Endpoint: POST /login/
   - Parâmetros (form-data):
      - email (string) – obrigatório
      - senha (string) – obrigatório

- Logout
   - Endpoint: POST /logout/
   - Parâmetros (form-data):
      - email (string) – obrigatório

- Edição de perfil (nome, e-mail, imagem)
   - Endpoint: PUT /usuario/<email>/editar/
   - Parâmetros (form-data ou JSON):
      - nome (string) – opcional
      - email (string) – opcional
      - imagem (file) – opcional

- Alteração de senha com confirmação
   - Endpoint: PUT /usuario/`email do usuário`/alterar-senha/
   - Parâmetros (JSON ou form-data):
      - senha_atual (string) – obrigatório
      - nova_senha (string) – obrigatório

Confirmação de e-mail (token via console)
   - Enviar token
      - Endpoint: POST /usuario/enviar-token/
      - Parâmetros (form-data):
         - email (string) – obrigatório

   - Validar token
      - Endpoint: POST /usuario/validar-token/
      - Parâmetros (form-data):
         - email (string) – obrigatório
         - token (string) – obrigatório

### 📖 Gerenciamento de Livros
- Listagem paginada de livros
   - Endpoint: GET /livros/`email do usuário`/
   - Parâmetros de URL (query params):
      - page (int) – número da página (opcional, padrão: 1)
      - page_size (int) – tamanho da página (opcional, padrão: 10)

- Busca por título
   - Parâmetro opcional: search
      - Exemplo: ?search=machado
  
- Filtro por ano de publicação
   - Parâmetros opcionais:
      - ano_min (int) – ano mínimo
      - ano_max (int) – ano máximo
      - Exemplo: ?ano_min=1900&ano_max=2000

- Ordenação por diversos critérios
   - Parâmetro opcional: order_by
   - Valores válidos:
      - titulo
      - ano
      * \- titulo (ordem decrescente)
      * \- ano (ordem decrescente)
      - Exemplo: ?order_by=-ano
    
### 🔒 Restrições de acesso
Apenas usuários autenticados podem visualizar os livros.

Se o usuário não confirmou o e-mail, ele verá apenas livros não validados.

## 🛠 Tecnologias Utilizadas

- **Backend**: Python 3.x, Django, Django REST Framework
- **Banco de Dados**: SQLite (padrão do Django)
- **Documentação**: Swagger/OpenAPI (via drf-yasg)

## ⚙️ Instalação e Configuração

1. **Clonar o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/api-compartilhamento-anotacoes.git
   cd api-compartilhamento-anotacoes

2. **Configurar ambiente virtual**
   ```bash
   python -m venv venv
   # Linux/Mac:
   source venv/bin/activate
   # Windows:
   venv\Scripts\activate

3. **Instalar dependências**
   ```bash
   pip install -r requirements.txt

4. **Migrar banco de dados**
   ```bash
   python manage.py migrate

5. **Iniciar servidor**
   ```bash
   python manage.py runserver

## 🧪 Testes

1. Execute os testes automatizados com:
   ```bash
   python manage.py test

## 📚 Documentação da API

A API possui documentação automática gerada com Swagger/OpenAPI:

Interface Swagger UI: http://localhost:8000/swagger/


Esquema OpenAPI (JSON): http://localhost:8000/api/schema/



