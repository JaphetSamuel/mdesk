from django.db import models
import math


class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=100)
    contact = models.CharField(max_length=100, unique=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nom+" "+self.prenoms

    @property
    def total(self):
        t = 0
        for commande in self.commande_set.all():
            t += commande.total_simple
        return t

    @property
    def total_plus_livraison(self):
        t = 0
        for commande in self.commande_set.all():
            t += commande.total_plus_livraison
        return t

    @property
    def avance(self):
        t = 0
        for commande in self.avance_set.all():
            t += commande.montant
        return t

    @property
    def solde(self):
        solde =  self.avance - self.total_plus_livraison
        return solde

    @property
    def doit(self):
        return self.solde

    @property
    def attente_de_livraison(self):
        return self.commande_set.filter(livre=False).count() >= 1


class Categorie(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label

class Produit(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    nom = models.CharField(max_length=100)
    infos = models.TextField(null=True, blank=True)
    prix = models.PositiveIntegerField(default=0)
    quantite_par_camion = models.PositiveIntegerField(default=1)

    def __str__(self): return self.nom

    @property
    def nombre_commande(self):
        return self.commande_set.count()

    class Meta:
        ordering = ['-pk']


class Commande(models.Model):
     client = models.ForeignKey(Client, on_delete=models.CASCADE)
     date = models.DateTimeField(auto_now_add=True)
     produit = models.ForeignKey(Produit, on_delete=models.CASCADE, null=True)
     quantite = models.PositiveIntegerField(default=0)
     livre = models.BooleanField(default=False)

     def __str__(self):
         return self.client.nom+' %s'%self.date

     @property
     def total_simple(self):
         return self.produit.prix * self.quantite

     @property
     def total_plus_livraison(self):
         prix_camion = 5000
         nombre_camions = math.ceil((self.quantite / self.produit.quantite_par_camion + 1))
         livraison = nombre_camions * prix_camion
         return self.total_simple + livraison


class Avance(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    montant = models.PositiveIntegerField(default=0)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s"%(self.client, self.date)

    class Meta:
        ordering = ['-date']
