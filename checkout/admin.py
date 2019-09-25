from django.contrib import admin

# Register your models here.
# from checkout.models import Vendas
# from eventos.models import Ingresso
#
#
# @admin.register(Vendas)
# class VendasAdmin(admin.ModelAdmin):
#     list_display = ('show', 'ingresso', 'usuario', 'valor', 'criado_em')
#
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "ingresso":
#             kwargs["queryset"] = Ingresso.objects.filter(vendido=False)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
#
#     # def __init__(self, *args, **kwargs):
#     #     super(VendasAdmin, self).__init__(*args, **kwargs)
