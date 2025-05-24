from django.db import models
from django.contrib.auth.models import User, Group
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

# Profile model to add extra information to the built-in User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Only set nom/prenom on creation
        Profile.objects.get_or_create(
            user=instance,
            defaults={
                'nom': instance.username,
                'prenom': instance.first_name or ""
            }
        )
    else:
        # Do not update profile fields blindly!
        try:
            profile = instance.profile
            profile.save()  # Just save if needed, do not overwrite fields
        except Profile.DoesNotExist:
            Profile.objects.create(
                user=instance,
                nom=instance.username,
                prenom=instance.first_name or ""
            )
class OffreEmploi(models.Model):
    TYPE_CONTRAT_CHOIX = [
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('Stage', 'Stage'),
        ('Alternance', 'Alternance'),
        ('Freelance', 'Freelance'),
    ]

    CATEGORIE_CHOIX = [
        ('Tech', 'Tech'),
        ('Design', 'Design'),
        ('Marketing', 'Marketing'),
        ('Finance', 'Finance'),
        ('RH', 'Ressources Humaines'),
        ('Commercial', 'Commercial'),
        ('Autre', 'Autre'),
    ]

    titre = models.CharField(max_length=255)
    entreprise = models.CharField(max_length=255)
    localisation = models.CharField(max_length=255)
    type_contrat = models.CharField(max_length=100, choices=TYPE_CONTRAT_CHOIX)
    categorie = models.CharField(max_length=100, choices=CATEGORIE_CHOIX)
    description = models.TextField()
    recruteur = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='offres')
    date_publication = models.DateTimeField(auto_now_add=True)
    salaire_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salaire_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    est_active = models.BooleanField(default=True)

    def __str__(self):
        return self.titre

    class Meta:
        ordering = ['-date_publication']

class Candidature(models.Model):
    STATUT_CHOIX = [
        ('en attente', 'En attente'),
        ('accepté', 'Accepté'),
        ('refusé', 'Refusé'),
    ]
    
    def cv_upload_path(instance, filename):
        # Générer un chemin de fichier unique pour chaque CV
        return f'cvs/{instance.candidat.user.username}/{filename}'
    
    statut_candidature = models.CharField(max_length=20, choices=STATUT_CHOIX, default='en attente')
    date_envoi = models.DateTimeField(auto_now_add=True)
    candidat = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='candidatures')
    offre = models.ForeignKey(OffreEmploi, on_delete=models.CASCADE)
    
    # Champ pour stocker le CV avec des validations
    cv = models.FileField(
        upload_to=cv_upload_path, 
        validators=[FileExtensionValidator(['pdf'])],
        max_length=255,
        null=True,
        blank=True
    )
    
    # Champ pour la lettre de motivation
    lettre_motivation = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.candidat.user.username} - {self.offre.titre}"
    
    def save(self, *args, **kwargs):
        # Validation supplémentaire avant sauvegarde
        if self.cv:
            # Limiter la taille du CV à 5 Mo
            if self.cv.size > 5 * 1024 * 1024:  # 5 Mo
                raise ValidationError("Le CV ne doit pas dépasser 5 Mo.")
        
        super().save(*args, **kwargs)

class Message(models.Model):
    contenu = models.TextField()
    candidature = models.ForeignKey(Candidature, on_delete=models.CASCADE)
    


    def __str__(self):
        return f"Message pour la candidature {self.candidature.id}"

class TableauBord(models.Model):
    date_jour = models.DateField()

    def __str__(self):
        return f"Tableau du {self.date_jour}"
    

    
