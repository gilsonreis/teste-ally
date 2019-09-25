from rest_framework import viewsets, status
from rest_framework.response import Response

from checkout.models import Vendas
from checkout.serializer import VendasSerializer


class VendasViewSet(viewsets.ModelViewSet):
    serializer_class = VendasSerializer
    queryset = Vendas.objects.all()
    http_method_names = ['post', 'options']
