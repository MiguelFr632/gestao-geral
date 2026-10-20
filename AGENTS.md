# Instruções do agente — Gestão Geral

## Visão do projeto

Aplicação Django 5.1 para cadastro de clientes e controle de produtos/estoque. A interface atual é o Django Admin; `/` redireciona para `/admin/`. O banco de desenvolvimento é SQLite em `data/db.sqlite3`, persistido pelo Docker Compose.

Árvore principal:

- `config/`: configuração Django, URLs e WSGI.
- `core/models.py`: modelos `Cliente` e `Produto` e normalização dos dados.
- `core/admin.py`: telas e listagens do Django Admin.
- `core/migrations/`: migrações versionadas do app `core`.
- `entrypoint.sh`: inicialização do container, migrações e criação do admin padrão.
- `Dockerfile`, `docker-compose.yml`: ambiente de desenvolvimento em container.
- `data/`: dados locais persistentes; não tratar o SQLite como arquivo descartável.

## Comandos de desenvolvimento e verificação

Use o ambiente virtual local, quando disponível:

```bash
./venv/bin/python manage.py check
./venv/bin/python manage.py test
./venv/bin/python manage.py makemigrations --check --dry-run
```

O repositório ainda não possui testes automatizados; atualmente `manage.py test` encontra zero testes. Ao mudar comportamento, acrescente testes em `core/tests.py` ou em um pacote `core/tests/` e informe claramente o que foi e não foi validado.

Para executar no modo documentado pelo projeto:

```bash
docker compose config
docker compose up --build
```

O serviço chama-se `web` e expõe a porta `8000`. Para operações Django dentro do container, use `docker compose exec web ...`.

## Regras para alterações

1. Leia o modelo, a migração e a configuração do Admin relacionados antes de editar. Preserve o estilo simples do projeto; não introduza uma arquitetura, dependência ou ferramenta de lint/teste sem necessidade concreta.
2. Mudanças de esquema devem vir acompanhadas de uma migração em `core/migrations/`. Inspecione `makemigrations --check --dry-run` e `migrate --plan` antes de aplicar alterações ao banco persistente.
3. **Proteja os dados locais.** Nunca apague, substitua, faça `flush`, recrie ou versione `data/db.sqlite3`. Não use `docker compose down -v`. Se uma operação puder alterar o banco existente, peça confirmação antes de executá-la.
4. `Cliente.clean()` normaliza o documento para dígitos; `Produto.clean()` normaliza o SKU para maiúsculas e espaços simples. Preserve essas regras e considere que operações em lote, como `bulk_create()`/`QuerySet.update()`, não executam `save()` nem a validação do modelo.
5. Ao alterar `list_editable` no Admin, confira as restrições do Django: os campos precisam estar em `list_display` e não podem ser o primeiro campo da lista.
6. Mantenha textos e labels da aplicação em português brasileiro e preserve os tipos de dados e restrições existentes, salvo mudança explícita do requisito.
7. Não exponha, copie ou reutilize credenciais, chaves ou dados pessoais reais em exemplos, logs, testes ou documentação.

## Segurança e escopo de implantação

O estado atual é **somente para desenvolvimento**: `DEBUG=True`, `ALLOWED_HOSTS=['*']`, `SECRET_KEY` fixa no código e `entrypoint.sh` cria um superusuário padrão. O entrypoint também executa `makemigrations` ao iniciar; isso é comportamento existente do protótipo, não um padrão de release. Migrações devem ser geradas e revisadas durante o desenvolvimento e aplicadas por uma etapa controlada, não criadas silenciosamente em cada inicialização. Não declare o projeto pronto para produção nem amplie o uso dessas configurações. Mudanças de implantação devem mover segredos para ambiente, restringir hosts, desativar debug e substituir a criação de credenciais padrão por configuração segura. A skill `django-deployment-safety` contém a checklist.

## Skills do projeto

- Use `django-model-change` para alterar `Cliente`, `Produto`, validação ou migrações.
- Use `django-admin-change` para alterar listagens, filtros, busca ou edição em lote no Admin.
- Use `django-deployment-safety` para Docker, configurações, credenciais ou qualquer discussão de implantação.

Ao concluir uma alteração, resuma arquivos modificados, comandos executados e limitações verificadas. Não afirme que os testes passaram se o comando encontrou zero testes.
