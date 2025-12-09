from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api import views as v

urlpatterns = [
    # Auth
    path("auth/login/", TokenObtainPairView.as_view()),
    path("auth/registro/", v.VistaRegistro.as_view()),
    
    # App
    path("juegos/", v.VistaListaJuegos.as_view()),
    path("squads/", v.VistaSquads.as_view()),
    path("squads/<int:pk>/", v.VistaDetalleSquad.as_view()),
    path("stats/", v.VistaEstadisticas.as_view()),
]