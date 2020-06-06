from django.contrib import admin
from .models import *

admin.site.name = 'Administration Caisse'
admin.site.site_header = 'Administration Caisse'
admin.site.site_title = 'Administration Caisse'


class CommandeInline(admin.TabularInline):
    model = Commande
    extra = 1

class AvanceInline(admin.TabularInline):
    model = Avance
    extra = 1


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['label']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['nom','prenoms','contact','total','total_plus_livraison','avance','doit','attente_de_livraison']
    inlines = [CommandeInline, AvanceInline]
    search_fields = ['contact']


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['nom','categorie','prix']


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['client','total_simple','date']

@admin.register(Avance)
class AvanceAdmin(admin.ModelAdmin):
    list_display = ['client','montant','date']
