from django.urls import path
from . import views
from .views import admin_dashboard
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('welcome/', views.welcome, name='welcome'), 
    path('register/', views.register_view, name='register'), 
    path('recruteur/', views.recruteur_home, name='recruteur_home'),
    path('recruteur/offres/', views.afficher_offres, name='recruteur_offres'),
    path('recruteur/publier', views.create_offre, name='create_offre'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('offres-candidat/', views.afficher_offres_candidat, name='offres_candidat'),
    path('logout/', views.logout_view, name='logout'),
    path('delete_offre/<int:offre_id>/', views.delete_offre, name='delete_offre'),
    path('offre/<int:offre_id>/postuler/', views.postuler, name='postuler'),
    path('profil/', views.profil_view, name='profil'),
    path('offres/', views.offres, name='offres'),
    path('modifier_candidature/<int:candidature_id>/', views.modifier_candidature, name='modifier_candidature'),
    path('recruteur/candidature/<int:candidature_id>/changer/', views.changer_statut_et_notifier, name='changer_statut_et_notifier'),
    path('supprimer_candidature/<int:candidature_id>/', views.supprimer_candidature, name='supprimer_candidature'),
    path('search/', views.search_offres, name='search_offres'),
    path('add-recruteur/', views.add_recruteur, name='add_recruteur'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('offre/<int:offre_id>/modifier/', views.modifier_offre, name='modifier_offre'),
   
]