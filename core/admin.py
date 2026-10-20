from django.contrib import admin
from .models import Cliente, Produto

admin.site.site_header = "Sistema de Gestão - Estoque e Clientes"
admin.site.site_title = "Admin Gestão"
admin.site.index_title = "Painel de Controle"

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'documento', 'telefone', 'email')
    search_fields = ('nome', 'documento', 'email', 'telefone')
    list_per_page = 25

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'quantidade', 'preco_custo', 'preco_venda')
    list_editable = ('quantidade', 'preco_custo', 'preco_venda')
    search_fields = ('codigo', 'nome')
    list_filter = ('quantidade',)
    list_per_page = 25