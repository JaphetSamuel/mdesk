from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import mixins
from .forms import *
from django.contrib import messages
from .models import *


class HomeView(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'caisse/home.html'
    
    def get_context_data(self, **kwargs):
        data = super(HomeView, self).get_context_data(**kwargs)
        data['most_produit_list'] = Produit.objects\
                .annotate(num_commande=Count('commande'))\
                .order_by('-num_commande')[:5]
        data['commande'] = sum(map(lambda x: x.total_plus_livraison, Commande.objects.all()))
        data['avance'] = sum(map(lambda c: c.montant, Avance.objects.only('montant')))
        data['clients']= Client.objects.all()
        return data


class ClientListView(generic.ListView):
    model = Client
    template_name = 'caisse/client_list.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('contact', None) is not None:
            self.queryset = self.get_queryset().filter(contact__contains=request.GET['contact'])
        if request.GET.get('nom', None) is not None:
            self.queryset = self.get_queryset().filter(nom__contains=request.GET['nom'])

        return super(ClientListView, self).get(request, *args, **kwargs)


class ClientCreateView(generic.CreateView):
    model = Client
    template_name = 'caisse/client_create.html'
    fields = ['nom','prenoms','contact']
    success_url = '/clients/'


class ClientUpdateView(generic.UpdateView):
    model = Client
    success_url = '/clients/'
    fields = ['nom','prenoms','contact']
    template_name = 'caisse/client_update.html'

    def get_context_data(self, **kwargs):
        data = super(ClientUpdateView, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            data['commande_formset'] = CommandeFormset(queryset=self.get_object()
                                                       .commande_set.all(), instance=self.object)
            data['avance_formset'] = AvanceFormset(queryset=self.get_object().avance_set.all(),
                                                   instance=self.object)
        elif self.request.method == 'POST':
            data['commande_formset'] = CommandeFormset(self.request.POST, instance=self.object)
            data['avance_formset'] = AvanceFormset(self.request.POST, instance=self.object)
        return data
    
    def form_valid(self, form):
        commande_formset = self.get_context_data()['commande_formset']
        avance_formset = self.get_context_data()['avance_formset']
        if commande_formset.is_valid() and avance_formset.is_valid():
            commande_instances = commande_formset.save()
            avance_instances = avance_formset.save()
        else:
            messages.error(self.request, "Veuillez remplir correctment le formulaire !")
            return super(ClientUpdateView, self).form_invalid(form)
        messages.success(self.request, "Modification sauvegardé !")
        return super(ClientUpdateView, self).form_valid(form)


class ClientDetailView(generic.DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        from django.utils.timezone import now
        data = super(ClientDetailView, self).get_context_data(**kwargs)
        data['now'] = now()
        return data


class ProduitListView(generic.ListView):
    model = Produit
    template_name = 'caisse/produit_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data= super(ProduitListView, self).get_context_data(object_list=object_list, **kwargs)
        data['categorie_list'] = Categorie.objects.all()
        return data

    def get(self, request, *args, **kwargs):
        if request.GET.get('categorie', None) is not None and request.GET['categorie'] != 't':
            self.queryset = self.get_queryset().filter(categorie=request.GET['categorie'])
        if request.GET.get('nom', None) is not None:
            self.queryset = self.get_queryset().filter(nom__contains=request.GET['nom'])

        return super(ProduitListView, self).get(request, *args, **kwargs)


class ProduitcreateView(generic.CreateView):
    model = Produit
    template_name = 'caisse/produit_create.html'
    success_url = '/produits/'
    fields = ['nom','categorie','prix']


class CategorieListView(generic.ListView):
    model= Categorie
