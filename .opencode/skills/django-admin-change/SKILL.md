---
name: django-admin-change
description: Use ao mudar a interface Django Admin, list_display, list_editable, filtros, buscas ou formulários dos modelos Cliente e Produto.
---

# Alterar o Django Admin

## Contexto

O projeto usa o Admin como interface principal. Os registros de `Cliente` e `Produto` são configurados em `core/admin.py`; a raiz redireciona para `/admin/` em `config/urls.py`.

## Procedimento

1. Leia `core/admin.py`, os campos e `Meta` dos modelos em `core/models.py`.
2. Ao mudar `list_display`, confira que cada item é um campo ou método existente.
3. Para `list_editable`, cada campo precisa aparecer em `list_display` e não pode ocupar a primeira posição. Não torne documento, SKU ou outros identificadores únicos editáveis em lote sem requisito explícito.
4. Para busca e filtros, escolha campos existentes e adequados ao volume. Não exponha campos pessoais além do que a tela realmente precisa.
5. Preserve labels e mensagens em português brasileiro. Se o Admin passar a depender de método/model property, teste também os casos de `None`/vazio.
6. Execute:

   ```bash
   ./venv/bin/python manage.py check
   ./venv/bin/python manage.py test core
   ```

7. Se não houver testes para Admin, informe isso e descreva a verificação manual segura. Não use o banco SQLite de produção ou dados pessoais reais para screenshots/testes.

## Atenção

`ProdutoAdmin.list_editable` permite alterar quantidade e preços diretamente na listagem. Mudanças nessa configuração alteram o fluxo de edição, não apenas a apresentação; registre esse impacto na resposta.
