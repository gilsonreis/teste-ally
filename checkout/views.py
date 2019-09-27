from django.shortcuts import render
from pagseguro.api import PagSeguroApi, PagSeguroApiTransparent, PagSeguroItem


# Create your views here.


def teste_pagseguro(request):
    pagseguro_api = PagSeguroApi(reference='id-unico-de-referencia-do-seu-sistema')
    item1 = PagSeguroItem(id='0001', description='Notebook Prata', amount='24300.00', quantity=1)
    item2 = PagSeguroItem(id='0002', description='Meu item 0002', amount='150.00', quantity=1, shipping_cost='25.00',
                          weight=500)
    pagseguro_api.add_item(item1)
    pagseguro_api.add_item(item2)

    api = PagSeguroApiTransparent()
    api.add_item(item1)

    sender = {'name': 'Jose Comprador', 'area_code': 11, 'phone': 56273440, 'email': 'comprador@uol.com.br',
              'cpf': '22111944785', }
    api.set_sender(**sender)

    shipping = {'street': "Av. Brigadeiro Faria Lima", 'number': 1384, 'complement': '5o andar',
                'district': 'Jardim Paulistano', 'postal_code': '01452002', 'city': 'Sao Paulo', 'state': 'SP',
                'country': 'BRA', }
    api.set_shipping(**shipping)

    api.set_payment_method('creditcard')
