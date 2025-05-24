from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Candidature
from .models import Message
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import Group
from .models import Profile, OffreEmploi  # Ajout de l'import de Profile et OffreEmploi
from .forms import OffreEmploiForm  # Assurez-vous que ce formulaire existe
from django.contrib.auth import logout
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Vue pour la connexion avec identifiant (nom d'utilisateur ou email)
def login_view(request):
    if request.method == 'POST':
        identifier = request.POST['identifier']
        password = request.POST['password']

        # Authentification par nom d'utilisateur
        user = authenticate(request, username=identifier, password=password)

        # Si échec, on essaie l'email
        if user is None:
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)

            # Redirection selon le rôle
            if user.is_superuser:
                return redirect('admin_dashboard')       
            elif user.groups.filter(name='Recruteur').exists():
                return redirect('recruteur_home')
            else:
                return redirect('welcome')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'candidatures/login.html')

def welcome(request):
    query = request.GET.get('q')  # récupère la recherche dans la barre
    
    if query:
        offres = OffreEmploi.objects.filter(titre__icontains=query)
    else:
        offres = OffreEmploi.objects.all()

    offres_postulees_ids = []
    candidature_par_offre = {}
    notifications = []

    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        candidatures = request.user.profile.candidatures.select_related('offre')

        for candidature in candidatures:
            offres_postulees_ids.append(candidature.offre.id)
            candidature_par_offre[candidature.offre.id] = candidature

            messages = Message.objects.filter(candidature=candidature)
            notifications.extend(messages)

    for offre in offres:
        offre.candidature = candidature_par_offre.get(offre.id)

    context = {
        'offres': offres,
        'offres_postulees_ids': offres_postulees_ids,
        'notifications': notifications,
        'query': query,  # 👈 ajoute query dans le contexte
    }

    return render(request, 'candidatures/candidat.html', context)


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.urls import reverse
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from .models import Candidature, Profile

@staff_member_required
def admin_dashboard(request):
    # 1. Choisir la section : 'stats', 'users', 'recruteurs', ou 'applications'
    section = request.GET.get('section', 'stats')

    # 2. Traitement des formulaires si POST
    if request.method == 'POST':
        action = request.POST.get('action')

        # ---- Gestion des UTILISATEURS ----
        if action == 'add_user':
            return add_user(request)
        elif action == 'edit_user':
            return edit_user(request)
        elif action == 'delete_user':
            return delete_user(request)

        # ---- Gestion des RECRUTEURS ----
        elif action == 'add_recruteur':
            return add_recruteur(request)
        elif action == 'delete_recruteur':
            return delete_recruteur(request)

        # ---- GESTION DES CANDIDATURES ----
        elif section == 'applications' and action == 'change_application_status':
            return change_application_status(request)

        # Redirection vers la même section après traitement
        return redirect(f"{reverse('admin_dashboard')}?section={section}")

    # 3. Construit le contexte pour le rendu GET
    context = {
        'section': section,
        'total_users': User.objects.count(),
        'total_recruiters': User.objects.filter(groups__name='Recruteur').count(),
        'total_candidatures': Candidature.objects.count(),
       'total_candidats': User.objects.filter(groups__name='Candidat').count()
 

    }

    # Chargement des données selon la section
    if section == 'users':
        context['users_list'] = User.objects.all().order_by('username')

    if section == 'recruiters':
        context['recruteurs'] = User.objects.filter(groups__name='Recruteur').order_by('username')

    if section == 'applications':
        context['applications_list'] = Candidature.objects.select_related('offre', 'candidat__user').order_by('-date_envoi')

    return TemplateResponse(request, 'candidatures/dashboard.html', context)

# Fonction pour ajouter un utilisateur
def add_user(request):
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    password = request.POST.get('password', '')

    if not username or not password:
        messages.error(request, "Nom d'utilisateur et mot de passe requis.")
    elif User.objects.filter(username=username).exists():
        messages.error(request, "Ce nom d'utilisateur existe déjà.")
    else:
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        messages.success(request, f"Utilisateur « {username} » créé avec succès.")
    return redirect(request.META.get('HTTP_REFERER'))

def add_message(request, type, message):
    if type == "success":
        messages.success(request, message)
    elif type == "error":
        messages.error(request, message)

# Fonction pour modifier un utilisateur
def edit_recruteur(request):
    user_id = request.POST.get('user_id')
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')

    try:
        user = User.objects.get(pk=user_id)
        if username != user.username and User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
        else:
            user.username = username
            user.email = email
            if password:
                user.set_password(password)
            user.save()
            messages.success(request, f"Recruteur « {username} » mis à jour avec succès.")
    except User.DoesNotExist:
        messages.error(request, "Recruteur introuvable.")
    
    return redirect(request.META.get('HTTP_REFERER'))

# Fonction pour supprimer un utilisateur
def delete_user(request):
    user_id = request.POST.get('user_id')
    try:
        user = User.objects.get(pk=user_id)
        if user == request.user:
            messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
        else:
            username = user.username
            user.delete()
            messages.success(request, f"Utilisateur « {username} » supprimé avec succès.")
    except User.DoesNotExist:
        messages.error(request, "Utilisateur introuvable.")
    
    return redirect(request.META.get('HTTP_REFERER'))

def edit_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')  # ← correspond à name="user_id"
        print("ID reçu:", user_id)

        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        try:
            user = User.objects.get(id=int(user_id))
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.success(request, "Utilisateur modifié avec succès.")
        except (User.DoesNotExist, ValueError, TypeError):
            messages.error(request, "Utilisateur non trouvé ou ID invalide.")

    return redirect('/dashboard/?section=users')

# Fonction pour ajouter un recruteur
def add_recruteur(request):
    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')

    if not username or not password:
        messages.error(request, "Nom d'utilisateur et mot de passe requis.")
    elif User.objects.filter(username=username).exists():
        messages.error(request, "Ce nom d'utilisateur existe déjà.")
    else:
        user = User.objects.create_user(username=username, email=email, password=password)
        group = Group.objects.get(name='Recruteur')
        user.groups.add(group)
        user.save()
        messages.success(request, f"Recruteur « {username} » ajouté avec succès.")
    
    return redirect(request.META.get('HTTP_REFERER'))

# Fonction pour supprimer un recruteur
def delete_recruteur(request):
    user_id = request.POST.get('user_id')
    try:
        user = User.objects.get(pk=user_id)
        if user == request.user:
            messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
        elif not user.groups.filter(name='Recruteur').exists():
            messages.error(request, "Cet utilisateur n'est pas un recruteur.")
        else:
            username = user.username
            user.delete()
            messages.success(request, f"Recruteur « {username} » supprimé avec succès.")
    except User.DoesNotExist:
        messages.error(request, "Utilisateur introuvable.")
    
    return redirect(request.META.get('HTTP_REFERER'))

# Fonction pour changer le statut d'une candidature
def change_application_status(request):
    cand_id = request.POST.get('candidature_id')
    new_status = request.POST.get('statut')
    candidature = get_object_or_404(Candidature, pk=cand_id)
    candidature.statut_candidature = new_status
    candidature.save()
    messages.success(request, "Statut de la candidature mis à jour.")
    
    return redirect(request.META.get('HTTP_REFERER'))

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Ce nom d'utilisateur est déjà utilisé.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Cet email est déjà utilisé.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                login(request, user)

                # Vérifie si c'est un recruteur
                if user.groups.filter(name='Recruteur').exists():
                    return redirect('recruteur_home')
                else:
                    return redirect('welcome')
        else:
            messages.error(request, "Les mots de passe ne correspondent pas.")

    return render(request, 'candidatures/login.html')

# Vue pour la page d'accueil après connexion ou inscription
@login_required
def supprimer_candidature(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id)
    candidature.delete()
    return redirect('welcome')

def modifier_candidature(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')  # Normalement inutile car @login_required

        # Vérifier que la candidature appartient bien au profil de l'utilisateur
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return redirect('offres')

        if candidature.candidat != profile:
            return redirect('offres')  # Empêcher la modification si ce n'est pas son dossier

        # Mise à jour des champs
        lettre_motivation = request.POST.get('lettre_motivation')
        cv = request.FILES.get('cv')

        candidature.lettre_motivation = lettre_motivation

        if cv:
            candidature.cv = cv  # Mettre à jour le CV seulement si l'utilisateur a uploadé un nouveau fichier

        candidature.save()

        return redirect('welcome')  # Redirection vers la page principale

    else:
        return redirect('welcome')

def changer_statut_candidature(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id)

    if request.method == 'POST':
        nouveau_statut = request.POST.get('statut')
        candidature.statut = nouveau_statut
        candidature.save()

        # Créer un message pour informer le candidat
        contenu_message = f"Votre candidature pour '{candidature.offre.titre}' a été mise à jour : {nouveau_statut}"
        Message.objects.create(
            contenu=contenu_message,
            candidature=candidature
        )

        return redirect('welcome')

def is_recruteur(user):
    return user.groups.filter(name='Recruteur').exists()

def create_offre(request):
    if request.method == 'POST':
        form = OffreEmploiForm(request.POST)
        if form.is_valid():
            try:
                profile = request.user.profile
                offre = form.save(commit=False)
                offre.recruteur = profile
                offre.save()
                messages.success(request, 'Offre ajoutée avec succès !')
                return redirect('recruteur_home')
            except Profile.DoesNotExist:
                messages.error(request, 'Profil recruteur non trouvé. Veuillez compléter votre profil.')
                return redirect('recruteur_home')
    return redirect('recruteur_home')

def afficher_offres(request):
    offres = OffreEmploi.objects.filter(recruteur=request.user.profile)
    return render(request, 'candidatures/recruteur.html', {'offres': offres})

def afficher_offres_candidat(request):
    offres = OffreEmploi.objects.filter(est_active=True)  # Seulement les offres actives
    if not offres:
        messages.info(request, "Aucune offre disponible.")
    return render(request, 'candidatures/candidat.html', {'offres': offres})

@login_required
def postuler(request, offre_id):
    offre = get_object_or_404(OffreEmploi, id=offre_id)

    if request.method == 'POST':
        # On récupère le profil du candidat
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            # Si pas de profil, rediriger quelque part (à toi de choisir)
            return redirect('welcome')

        lettre_motivation = request.POST.get('lettre_motivation')
        cv = request.FILES.get('cv')

        # Vérifier si une candidature existe déjà pour cette offre
        candidature, created = Candidature.objects.get_or_create(
            candidat=profile,
            offre=offre,
            defaults={
                'lettre_motivation': lettre_motivation,
                'cv': cv
            }
        )

        if not created:
            # Si déjà existante, mettre à jour
            candidature.lettre_motivation = lettre_motivation
            if cv:
                candidature.cv = cv
            candidature.save()

        return redirect('welcome')  # Redirection après postulation/modification

    return redirect('welcome')

def logout_view(request):
    logout(request)  # Cela détruit la session
    return redirect('login') 

def delete_offre(request, offre_id):
    offre = get_object_or_404(OffreEmploi, id=offre_id)
    if request.method == 'POST':
        offre.delete()
        messages.success(request, 'Offre supprimée avec succès.')
    return redirect('recruteur_home')

def offres(request):
    offres = OffreEmploi.objects.all()  # Ou selon ta logique de récupération des offres
    return render(request, 'candidatures/candidat.html', {'offres': offres})

@login_required



@login_required
@user_passes_test(is_recruteur)
def changer_statut_et_notifier(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id)
    # Nouveau statut envoyé par le formulaire
    nouveau_statut = request.POST.get('statut')

    # Vérifier validité
    if nouveau_statut not in dict(Candidature.STATUT_CHOIX):
        messages.error(request, "Statut invalide.")
        return redirect('recruteur_home')

    # Mettre à jour la candidature
    candidature.statut_candidature = nouveau_statut
    candidature.save()

    # Envoyer la "notification" via un Message
    contenu = (
        f"Bonjour {candidature.candidat.user.first_name or candidature.candidat.user.username},\n"
        f"Le statut de votre candidature pour « {candidature.offre.titre} » a été mis à jour : "
        f"{dict(Candidature.STATUT_CHOIX)[nouveau_statut]}."
    )
    Message.objects.create(candidature=candidature, contenu=contenu)

    messages.success(request, "Statut mis à jour et candidat notifié.")
    return redirect('recruteur_home')
@user_passes_test(is_recruteur)
def recruteur_home(request):
    # 1 Le formulaire + les offres du recruteur
    form = OffreEmploiForm()
    offres = OffreEmploi.objects.filter(recruteur=request.user.profile)

    # 2 On récupère *toutes* les candidatures pour *ces* offres
    candidatures = Candidature.objects.filter(offre__in=offres).order_by('-date_envoi')

    # 3 On envoie *les deux* à ton template
    return render(request, 'candidatures/recruteur.html', {
        'form': form,
        'offres': offres,
        'candidatures': candidatures,
    })

def search_offres(request):
    poste = request.GET.get('poste', '')
    type_annonce = request.GET.get('type', '')

    offres = OffreEmploi.objects.all()
    if poste:
        offres = offres.filter(titre__icontains=poste)
    if type_annonce:
        offres = offres.filter(type_contrat__iexact=type_annonce)

    return render(request, 'candidatures/candidat.html', {'offres': offres})

@login_required
def profil_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    candidatures = Candidature.objects.filter(candidat=profile).select_related('offre')

    for c in candidatures:
        if not c.cv:
            c.cv_url = ""
        else:
            try:
                c.cv_url = c.cv.url
            except ValueError:
                c.cv_url = ""

    return render(request, 'candidatures/profil.html', {
        'profile': profile,
        'candidatures': candidatures,
    })

@login_required
def edit_profile(request):
    # Get the user's profile
    profile = request.user.profile

    # Get user's candidatures for display
    candidatures = profile.candidatures.all()

    # If the request method is POST, process the form submission
    if request.method == 'POST':
        try:
            # Get the data from the POST request
            nom = request.POST.get('nom', profile.nom)
            prenom = request.POST.get('prenom', profile.prenom)
            numero_telephone = request.POST.get('numero_telephone', profile.numero_telephone)
            email = request.POST.get('email', profile.user.email)

            # Update profile fields if the data has changed
            if nom != profile.nom:
                profile.nom = nom  # Update nom only if it has changed

            profile.prenom = prenom
            profile.numero_telephone = numero_telephone

            # Update email if changed
            if email != profile.user.email:
                # Check if the new email is already taken by another user
                if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                    messages.error(request, _("Cet email est déjà utilisé par un autre utilisateur."))
                    return render(request, 'candidatures/edit_profile.html', {
                        'profile': profile,
                        'candidatures': candidatures
                    })
                profile.user.email = email

            # Save changes
            profile.user.save()
            profile.save()

            # Add success message
            messages.success(request, _("Votre profil a été mis à jour avec succès."))

            # Redirect to profile view
            return redirect('profil')

        except Exception as e:
            messages.error(request, _("Une erreur s'est produite: ") + str(e))

    # Render the edit profile form
    return render(request, 'candidatures/profil.html', {
        'profile': profile,
        'candidatures': candidatures
    })

@login_required
def detail_candidature(request, candidature_id):
    candidature = get_object_or_404(Candidature, id=candidature_id)

    # S'assurer que seul le candidat concerné ou un recruteur peut y accéder
    if not request.user.is_superuser and request.user != candidature.candidat.user:
        if not request.user.groups.filter(name='Recruteur').exists():
            return HttpResponse("Non autorisé", status=403)

    return render(request, 'candidatures/detail_candidature.html', {
        'candidature': candidature
    })

def modifier_offre(request, offre_id):
    offre = get_object_or_404(OffreEmploi, id=offre_id)
    
    # Vérifier que l'offre appartient au recruteur connecté
    if offre.recruteur != request.user.profile:
        messages.error(request, "Vous n'êtes pas autorisé à modifier cette offre.")
        return redirect('recruteur_home')
    
    if request.method == 'POST':
        # Récupération des données du formulaire
        offre.titre = request.POST.get('titre', offre.titre)
        offre.entreprise = request.POST.get('entreprise', offre.entreprise)
        offre.localisation = request.POST.get('localisation', offre.localisation)
        offre.type_contrat = request.POST.get('type_contrat', offre.type_contrat)
        offre.categorie = request.POST.get('categorie', offre.categorie)
        offre.description = request.POST.get('description', offre.description)
        
        # Conversion des valeurs numériques
        try:
            offre.salaire_min = int(request.POST.get('salaire_min', offre.salaire_min))
            offre.salaire_max = int(request.POST.get('salaire_max', offre.salaire_max))
        except ValueError:
            messages.error(request, "Les salaires doivent être des nombres entiers.")
            return redirect('recruteur_home')
        
        # Sauvegarde des modifications
        offre.save()
        messages.success(request, f"L'offre '{offre.titre}' a été modifiée avec succès.")
        
    return redirect("recruteur_home")