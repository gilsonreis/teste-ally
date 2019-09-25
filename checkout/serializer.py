from rest_framework import serializers

from checkout.models import Vendas


class VendasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendas
        fields = '__all__'
        read_only_fields = ('valor', )
