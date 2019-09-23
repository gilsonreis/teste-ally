from django.contrib import admin

from eventos.models import Teatro, Show, Ingresso


@admin.register(Teatro)
class TeatroAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ['nome']


class IngressoInline(admin.TabularInline):
    model = Ingresso


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    inlines = [IngressoInline]
    fieldsets = (
        (None, {
            'fields': (('nome', 'data_evento'), 'descricao',)
        }),
        (None, {
            'fields': (('teatro', 'valor',), ('quantidade_lugares', 'status'),)
        })
    )

    list_display = ('nome', 'teatro', 'valor', 'status', 'data_evento')
    search_fields = ('nome',)
    list_filter = ('teatro__nome', 'valor', 'status',)
    date_hierarchy = 'data_evento'


@admin.register(Ingresso)
class IngressoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'list_teatro', 'show', 'vendido',)
    search_fields = ('codigo', 'show__nome', 'show__teatro__nome')
    list_filter = ('show__teatro__nome', 'vendido',)

    def list_teatro(self, obj):
        return obj.show.teatro.nome

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["codigo"]
        else:
            return []

