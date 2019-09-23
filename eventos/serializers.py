from abc import ABC

from rest_framework import serializers

from .models import Teatro, Show, Ingresso


class TeatroDisponiveisSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(max_length=60, read_only=True)

    class Meta:
        model = Teatro
        fields = ("id", 'nome')


class ShowIngressosDisponiveisSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(max_length=60, read_only=True)
    data_evento = serializers.DateTimeField(read_only=True)
    codigo_ingresso = serializers.CharField(max_length=16, read_only=True)
    qtde_disponiveis = serializers.IntegerField(read_only=True)

    class Meta:
        model = Show
        fields = ("id", 'nome', 'data_evento', 'codigo_ingresso', 'qtde_disponiveis')


class TeatroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teatro
        fields = '__all__'


class ShowSerializer(serializers.ModelSerializer):
    teatro = TeatroSerializer(read_only=True)
    teatro_id = serializers.PrimaryKeyRelatedField(queryset=Teatro.objects.all(), write_only=True, source='teatro')

    class Meta:
        model = Show
        fields = ('id', 'nome', 'descricao', 'data_evento', 'teatro', 'valor', 'quantidade_lugares', 'status', 'teatro',
                  'teatro_id',)


class IngressoSerializer(serializers.ModelSerializer):
    show = ShowSerializer(read_only=True)
    show_id = serializers.PrimaryKeyRelatedField(queryset=Show.objects.all(), write_only=True, source='show')

    class Meta:
        model = Ingresso
        fields = ('id', 'codigo', 'show', 'show_id',)
