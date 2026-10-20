import re
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError

class Cliente(models.Model):
    nome = models.CharField("Nome", max_length=255)
    documento = models.CharField(
        "CPF/CNPJ",
        max_length=20,
        unique=True,
        help_text="Digite apenas números ou com pontuação (será salvo apenas com números)."
    )
    telefone = models.CharField("Telefone", max_length=30, blank=True, null=True)
    email = models.EmailField("E-mail", blank=True, null=True)
    endereco = models.TextField("Endereço", blank=True, null=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']

    def clean(self):
        super().clean()
        if self.documento:
            # Mantém apenas os dígitos numéricos
            self.documento = re.sub(r'\D', '', self.documento)
            if not self.documento:
                raise ValidationError({'documento': 'O documento deve conter números válidos.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.documento})"


class Produto(models.Model):
    nome = models.CharField("Nome", max_length=255)
    codigo = models.CharField(
        "Código / SKU",
        max_length=100,
        unique=True,
        help_text="Será convertido automaticamente para MAIÚSCULAS e sem espaços extras."
    )
    quantidade = models.IntegerField("Quantidade Atual", default=0)
    preco_custo = models.DecimalField(
        "Preço de Custo (R$)",
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    preco_venda = models.DecimalField(
        "Preço de Venda (R$)",
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Estoque (Produtos)"
        ordering = ['nome']

    def clean(self):
        super().clean()
        if self.codigo:
            # Remove espaços duplicados/nas pontas e converte para maiúsculas
            self.codigo = " ".join(self.codigo.strip().upper().split())

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.codigo}] {self.nome}"