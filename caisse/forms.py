from django import forms
from .models import *

CommandeFormset = forms.inlineformset_factory(parent_model=Client,
                                              model=Commande, extra=1,
                                              fields=['produit','quantite','livre'], can_delete=True)

AvanceFormset = forms.inlineformset_factory(parent_model=Client,
                                            model=Avance, extra=1, fields=['montant'], can_delete=True)