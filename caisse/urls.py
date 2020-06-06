from django.urls import path
from .apps  import CaisseConfig
from .views import *



app_name = CaisseConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/ajouter/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/modifier', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/details', ClientDetailView.as_view(template_name='caisse/client_detail.html'), name='client_details'),

    path('produits/', ProduitListView.as_view(), name='produit_list'),
    path('produit/ajouter/', ProduitcreateView.as_view(), name='produit_create'),

    path('categories/', CategorieListView.as_view(template_name='caisse/categorie_list.html'), name='categorie_list')
]