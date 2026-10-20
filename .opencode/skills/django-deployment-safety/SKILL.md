---
name: django-deployment-safety
description: Use para analisar ou alterar Docker, settings, variáveis de ambiente, credenciais, exposição de rede ou prontidão de produção neste projeto.
---

# Segurança de execução e implantação

## Estado conhecido

O repositório é um protótipo de desenvolvimento, não uma implantação pronta para produção. Atualmente:

- `config/settings.py` contém `DEBUG=True`, `ALLOWED_HOSTS=['*']` e uma chave secreta fixa.
- `entrypoint.sh` cria um superusuário padrão com credenciais fixas se ainda não existir.
- `entrypoint.sh` executa `makemigrations core` em cada inicialização, o que não deve ser tratado como procedimento de release.
- `docker-compose.yml` mapeia o código-fonte em `/app` e publica a porta `8000`.
- `./data:/app/data` persiste o SQLite fora do ciclo de vida do container.
- O container inicia o servidor de desenvolvimento Django (`runserver`).

## Checklist antes de qualquer recomendação de produção

1. Carregar `SECRET_KEY` e credenciais por ambiente/secret store; falhar com mensagem segura se estiverem ausentes.
2. Desativar debug e restringir `ALLOWED_HOSTS` a hosts explicitamente aprovados.
3. Remover a criação automática de conta padrão; provisionar administrador por procedimento separado e credenciais rotacionáveis.
4. Retirar a geração automática de migrações do entrypoint; gerar, revisar e aplicar migrações como etapa explícita e controlada.
5. Substituir `runserver` por servidor WSGI/ASGI apropriado; configurar HTTPS, cookies seguros, CSRF, hosts e logs.
6. Rever volume/permissões, backup, recuperação e política de migrações para SQLite; avaliar outro banco somente se requisitos justificarem.
7. Executar `python manage.py check --deploy` num ambiente de configuração de produção e resolver os avisos aplicáveis.

## Proteção de dados durante desenvolvimento

- Trate `data/db.sqlite3` como dado do usuário. Não apague, substitua, faça `flush`, use `docker compose down -v` nem recrie o volume sem autorização explícita.
- Antes de uma migração potencialmente destrutiva, mostre `migrate --plan`, explique o impacto e solicite confirmação.
- `docker compose config` e `docker compose up --build` são verificações de desenvolvimento; não provam segurança ou prontidão de produção.
- Nunca inclua senha, chave ou cópia de base real em documentação, testes ou commits.
