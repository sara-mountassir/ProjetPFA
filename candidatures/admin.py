from django.contrib import admin
from .models import Profile, OffreEmploi, Candidature, Message, TableauBord


# Enregistrer les modèles avec leurs configurations personnalisées
admin.site.register(Profile)
admin.site.register(OffreEmploi)
admin.site.register(Candidature)
admin.site.register(Message)
admin.site.register(TableauBord)