---
name: django-model-change
description: Use ao criar ou alterar modelos, campos, normalização, validação ou migrações dos modelos Cliente e Produto deste projeto Django.
---

# Alterar modelos e dados

## Contexto deste projeto

- Os modelos ficam em `core/models.py`; migrações em `core/migrations/`.
- `Cliente.documento` é único e sua normalização mantém somente dígitos em `clean()`.
- `Produto.codigo` é único e sua normalização remove espaços extras e converte para maiúsculas em `clean()`.
- Os dois modelos chamam `full_clean()` em `save()`. Operações em lote (`bulk_create`, `QuerySet.update`) não percorrem esse fluxo.
- O banco local `data/db.sqlite3` contém dados persistentes e não pode ser apagado ou substituído como parte de uma tarefa comum.

## Procedimento

1. Leia o modelo, `core/migrations/0001_initial.py`, `core/admin.py` e os usos do campo antes de alterar o esquema.
2. Confirme o requisito e escolha o tipo/tamanho/default/nullability do campo. Não adicione validação de CPF/CNPJ, limites de estoque ou regras comerciais que não tenham sido pedidos.
3. Atualize modelo, migração e testes juntos. Teste explicitamente normalização, unicidade, valores em branco e comportamento de atualização pertinente à mudança.
4. Inspecione a migração gerada; procure remoções ou operações destrutivas inesperadas.
5. Verifique com:

   ```bash
   ./venv/bin/python manage.py check
   ./venv/bin/python manage.py makemigrations --check --dry-run
   ./venv/bin/python manage.py test core
   ```

   Se o ambiente virtual não existir, use `python manage.py ...` no ambiente configurado ou `docker compose exec web python manage.py ...`.

6. Antes de aplicar migrações ao banco local existente, mostre o plano e peça confirmação. Testes podem usar o banco de teste isolado do Django.

## Não fazer

- Não editar diretamente `data/db.sqlite3` nem incluí-lo no Git.
- Não apagar ou reescrever migrações aplicadas sem pedido explícito e plano de recuperação.
- Não presumir que `save()`/`clean()` seja executado por operações em lote.
- Não declarar validação completa com base apenas em `manage.py check`.
