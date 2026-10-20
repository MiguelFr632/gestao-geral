# Sistema de Gestão de Estoque e Clientes

Aplicação simples e portátil desenvolvida em **Python (Django)** com banco de dados **SQLite** e empacotada com **Docker**, focada no gerenciamento direto de clientes e controle de estoque através do painel Django Admin.

---

## Funcionalidades

* **Gestão de Clientes:**
  * Cadastro de Nome, CPF/CNPJ (obrigatório e único), Telefone, E-mail e Endereço.
  * Normalização automática do CPF/CNPJ (remove pontuações e salva apenas os números para evitar duplicidades).
  * Busca rápida por nome, documento, e-mail ou telefone.
* **Controle de Estoque (Produtos):**
  * Cadastro de Nome, Código/SKU (obrigatório e único), Quantidade Atual, Preço de Custo e Preço de Venda.
  * Normalização automática do Código/SKU (converte para letras maiúsculas e remove espaços extras).
  * Edição rápida de quantidades e preços diretamente na tabela de listagem do painel.
* **Persistência Isolada:**
  * O arquivo do banco SQLite fica armazenado em `./data/db.sqlite3`, facilitando o backup e a portabilidade entre máquinas via Docker.

---

## Estrutura do Projeto

```text
gestao-estoque/
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── manage.py
├── .gitignore
├── README.md
├── data/                  # Volume onde o banco SQLite (db.sqlite3) é salvo
├── config/                # Configurações globais do Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── core/                  # App principal (Models e configuração do Admin)
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    └── migrations/
        └── __init__.py
```

---

## Como Rodar com Docker (Recomendado para qualquer PC)

Basta ter o **Docker** e o **Docker Compose** instalados na máquina.

1. Na pasta raiz do projeto, suba o container:
   ```bash
   docker compose up --build -d
   ```

2. O script de inicialização (`entrypoint.sh`) irá automaticamente:
   * Criar a pasta `data/` (se não existir).
   * Criar e aplicar as migrações do banco SQLite.
   * Criar um superusuário padrão (caso o banco seja novo).
   * Iniciar o servidor na porta `8000`.

3. Acesse no navegador:
   * **URL:** `http://localhost:8000`
   * **Usuário padrão:** `admin`
   * **Senha padrão:** `admin123`

### Comandos Úteis do Docker

* **Ver logs em tempo real:**
  ```bash
  docker compose logs -f
  ```
* **Parar o sistema:**
  ```bash
  docker compose down
  ```
* **Criar um novo usuário admin manualmente via container:**
  ```bash
  docker compose exec web python manage.py createsuperuser
  ```

---

## Como Rodar Localmente (Desenvolvimento no Debian/Ubuntu)

Caso queira rodar fora do Docker durante o desenvolvimento:

1. Instale o módulo de ambientes virtuais e o gerenciador de pacotes do Python (se ainda não tiver):
   ```bash
   sudo apt update && sudo apt install -y python3-venv python3-pip
   ```

2. Crie a pasta de dados, o ambiente virtual e instale as dependências:
   ```bash
   mkdir -p data
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Aplique as migrações no banco SQLite e crie seu usuário de acesso:
   ```bash
   python manage.py makemigrations core
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

5. Acesse no navegador: `http://localhost:8000`

---

## Versionamento com Git e Pasta de Dados (`data/`)

O arquivo `.gitignore` já está configurado para ignorar o ambiente virtual (`venv/`), caches do Python e os arquivos de banco de dados (`.sqlite3` e `.db`).

Como o Git não versiona pastas vazias, se quiser que a pasta `data/` já seja criada automaticamente ao dar `git clone` em outro computador (porém sem enviar o seu arquivo `db.sqlite3`), crie um arquivo `.gitkeep` dentro dela:

```bash
touch data/.gitkeep
```

---

## Backup e Portabilidade dos Dados

Todo o banco de dados do sistema fica concentrado em um único arquivo: `data/db.sqlite3`.

* **Para fazer backup:** Basta copiar o arquivo `data/db.sqlite3` para um local seguro.
* **Para levar o sistema com os dados cadastrados para outro PC:** Copie a pasta do projeto incluindo o arquivo `data/db.sqlite3` e execute `docker compose up -d`.
* **Para subir o sistema zerado em outro PC:** Basta clonar o repositório pelo Git (que ignora o arquivo do banco) e executar `docker compose up -d`.