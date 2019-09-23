from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from core.models import TimestampableMixin

import requests

STATUS_SHOW = (
    (1, 'Ativo'),
    (2, 'Inativo'),
    (3, 'Cancelado'),
)


class Teatro(TimestampableMixin):
    nome = models.CharField(max_length=100, verbose_name="Nome")

    class Meta:
        verbose_name = "Teatro"
        verbose_name_plural = "Teatros"
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class Show(TimestampableMixin):
    nome = models.CharField(max_length=150, verbose_name="Nome")
    descricao = models.TextField(null=True, blank=True, verbose_name="Descrição")
    data_evento = models.DateTimeField(verbose_name="Data do Show")
    teatro = models.ForeignKey(Teatro, on_delete=models.CASCADE, related_name="shows")
    valor = models.DecimalField(verbose_name="Valor do ingresso", max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    quantidade_lugares = models.PositiveIntegerField(verbose_name="Quantidade máxima")
    status = models.SmallIntegerField(verbose_name="Status", choices=STATUS_SHOW, default=1)

    class Meta:
        verbose_name = "Show"
        verbose_name_plural = "Shows"
        ordering = ('data_evento',)

    def __str__(self):
        return '{}, {} em {}'.format(self.nome, self.teatro.nome, self.data_evento.strftime('%d/%m/%Y às %H:%M:%S'))


class Ingresso(models.Model):
    codigo = models.CharField(verbose_name='Codigo do Ingresso', max_length=16, null=True, blank=True,
                              help_text="Máximo de 16 caracteres. Deixe em branco para gerar automáticamente.")
    show = models.ForeignKey(Show, on_delete=models.PROTECT, related_name="ingressos")
    vendido = models.BooleanField(verbose_name="Vendido?", default=False)

    class Meta:
        verbose_name = "Ingresso"
        verbose_name_plural = "Ingressos"

    def __str__(self):
        return self.codigo

    def save(self, *args, **kwargs):
        if not self.codigo:
            url = 'https://helloacm.com/api/random/?n=16'  # texto randomico com 16 chars, representando codigo do ingresso
            response = requests.get(url)
            self.codigo = response.json()

        super(Ingresso, self).save(*args, **kwargs)
