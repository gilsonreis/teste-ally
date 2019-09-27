from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from eventos.models import Teatro, Show, Ingresso
from .serializers import TeatroSerializer, ShowSerializer, IngressoSerializer, TeatroDisponiveisSerializer, \
    ShowIngressosDisponiveisSerializer


class ShowIngressosDispioViewSet(viewsets.ModelViewSet):
    serializer_class = ShowSerializer
    queryset = Show.objects.all()


class TeatroViewSet(viewsets.ModelViewSet):
    serializer_class = TeatroSerializer
    queryset = Teatro.objects.all()

    @action(detail=False, methods=['get'], url_path='shows-disponiveis')
    def teatros_disponiveis(self, request):
        sql = """
                     select
                        t.id,
                        t.nome
                    from
                        eventos_teatro t
                    inner join eventos_show s on
                        t.id = s.teatro_id
                    inner join eventos_ingresso i on
                        s.id = i.show_id
                    where
                        s.status = 1 and
                        (
                            select count(id)
                        from
                            eventos_ingresso ei
                        where
                            ei.show_id = s.id
                            and ei.vendido = false) > 0
                    group by
                        t.id,
                        t.nome;       
                """

        teatros = Teatro.objects.raw(sql)

        serializer = TeatroDisponiveisSerializer(teatros, many=True)
        return Response(serializer.data)


class ShowViewSet(viewsets.ModelViewSet):
    serializer_class = ShowSerializer
    queryset = Show.objects.all()

    @action(detail=False, methods=['get'], url_path='ingressos-disponiveis-por-teatro/(?P<pk>[^/.]+)')
    def ingressos_disponiveis(self, request, pk):
        sql = """
            select
                s.id,
                s.nome,
                (s.quantidade_lugares - (select count(id)
                from
                    eventos_ingresso ei
                where
                    ei.show_id = s.id
                    and ei.vendido = true)) as qtde
            from
                eventos_show s
            inner join eventos_ingresso i on
                s.id = i.show_id
            where
                s.status = 1
                and (
                    select count(id)
                from
                    eventos_ingresso ei
                where
                    ei.show_id = s.id
                    and ei.vendido = false) > 0
                and s.teatro_id = %s
                group by s.id, s.nome
        """

        shows = Show.objects.raw(sql, [pk], translations={"id": "id", "nome": "nome", "data_evento": "data_evento",
                                                         "codigo": "codigo_ingresso", "qtde": "qtde_disponiveis"})
        serializer = ShowIngressosDisponiveisSerializer(shows, many=True)
        return Response(serializer.data)


class IngressoViewSet(viewsets.ModelViewSet):
    serializer_class = IngressoSerializer
    queryset = Ingresso.objects.all()
