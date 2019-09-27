from django.contrib.auth.models import User
from pagseguro.models import Checkout
from rest_framework import viewsets, status
from pagseguro.api import PagSeguroApi, PagSeguroApiTransparent, PagSeguroItem

from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from checkout.models import Vendas
from checkout.serializer import VendasSerializer
from eventos.models import Ingresso, Show


class VendasViewSet(viewsets.ModelViewSet):
    serializer_class = VendasSerializer
    queryset = Vendas.objects.all()
    http_method_names = ['post', 'options']


class CheckoutViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], url_path='pagseguro/retornar-session-id')
    def pagseguro_retornar_sessao_id(self, request):
        api = PagSeguroApiTransparent()
        data = api.get_session_id()
        data = {"session_id": data['session_id']}
        return Response(data)

    @action(detail=False, methods=['post'], url_path='pagseguro/realizar-pagamento/evento/(?P<show_id>[^/.]+)')
    def pagseguro_do_checkout(self, request, show_id):
        api = PagSeguroApiTransparent()

        ingresso = self.get_ingresso_disponvel(show_id)
        item = PagSeguroItem(id=ingresso.codigo, description='Ingresso do show {}'.format(ingresso.show.nome),
                             amount=ingresso.show.valor, quantity=1)
        api.add_item(item)

        api.set_payment_method('creditcard')  # usando cartão de crédito

        # dados do comprador. Deve vir no post ou do banco. Pra facilitar o teste, coloquei fixo.
        comprador = {'name': 'Tio Patinhas', 'area_code': 41, 'phone': 987654321,
                     'email': 'c81695396700179432922@sandbox.pagseguro.com.br',
                     'cpf': '22111944785', }
        api.set_sender(**comprador)

        # dados do pedido e do comprador. Deve vir no post ou do banco. Pra facilitar o teste, coloquei fixo.
        pedido = {'quantity': 1, 'value': ingresso.show.valor, 'name': 'Tio Patinhas', 'birth_date': '27/10/1987',
                  'cpf': '22111944785', 'area_code': 11, 'phone': 56273440, 'no_interest_quantity': 5}
        api.set_creditcard_data(**pedido)

        # dados do endereço do comprador. Deve vir no post ou do banco. Pra facilitar o teste, coloquei fixo.
        endereco = {'street': 'Av. Sete de setembro', 'number': 123, 'district': 'Centro',
                    'postal_code': '01234500', 'city': 'Curitiba', 'state': 'PR', 'country': 'BRA', }
        api.set_creditcard_billing_address(**endereco)

        shipping = {'street': "Av. Brigadeiro Faria Lima", 'number': 1384, 'complement': '5o andar',
                    'district': 'Jardim Paulistano', 'postal_code': '01452002', 'city': 'Sao Paulo', 'state': 'SP',
                    'country': 'BRA', }
        api.set_shipping(**shipping)

        # cartão adicionado via token gerado pela aplicação frontend
        api.set_creditcard_token(request.POST.get('card_token'))

        # adicionando o hash do usuario que vem via post, da aplicação frontend
        api.set_sender_hash(request.POST.get('sender_hash'))
        data = api.checkout()

        checkout = Checkout.objects.filter(code=data['transaction']['code']).get()

        # a id do usuario logado vem via POST, na aplicação frontend
        id_usuario = request.POST.get('id_usuario')
        usuario = User.objects.filter(id=id_usuario).get()
        self.salvar_venda(ingresso, checkout, usuario)

        # atualizando ingresso caso vendido == False
        if not ingresso.vendido:
            ingresso.vendido = True
            ingresso.save()

        return Response(data)

    def get_ingresso_disponvel(self, show_id):
        ingresso = Ingresso.objects.filter(vendido=False,
                                           show_id=show_id).first()  # pegando ingresso que ainda não foi vendido

        if not ingresso:  # caso não tenha nenhum ingresso disponível no banco, verificar se existe lugar vazio no show
            ingressos_vendidos = Ingresso.objects.filter(vendido=True, show_id=show_id).count()
            show = Show.objects.filter(pk=show_id).get()

            if show.quantidade_lugares > ingressos_vendidos:
                ingresso = self.salvar_novo_ingresso(show)
            else:
                raise ValidationError("Não existe mais ingressos disponíveis para esse show.")

        return ingresso

    def salvar_novo_ingresso(self, show):
        ingresso = Ingresso()
        ingresso.show = show
        ingresso.vendido = False
        ingresso.save()

        return ingresso

    def salvar_venda(self, ingresso, checkout, usuario):
        venda = Vendas()
        venda.ingresso = ingresso
        venda.checkout = checkout
        venda.usuario = usuario
        venda.valor = ingresso.show.valor
        venda.save()

        return venda
