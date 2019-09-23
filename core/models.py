from django.db import models


class TimestampableMixin(models.Model):
    criado_em = models.DateTimeField(auto_now=False, auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True
