from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from pagseguro.models import Checkout
from rest_framework.exceptions import ValidationError

from core.models import TimestampableMixin
from eventos.models import Ingresso, Show


class Vendas(TimestampableMixin):
    ingresso = models.ForeignKey(Ingresso, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"

    def __str__(self):
        return '{} em {}, de {}'.format(self.ingresso.codigo, self.ingresso.show.nome, self.usuario.username)

    def save(self, *args, **kwargs):
        print(vars(self.ingresso))
        if self.ingresso.vendido:  # validando se ingresso informado já foi vendido anteriormente.
            raise ValidationError("O ingresso {} já foi vendido!".format(self.ingresso.codigo))

        ingresso = self.ingresso
        ingresso.valor = self.ingresso.show.valor  # Atribuir valor do show a venda, para controle posterior.
        ingresso.save()  # alterando o valor do ingresso para valor do show.
        super(Vendas, self).save(*args, **kwargs)
