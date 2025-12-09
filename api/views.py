from django.utils import timezone
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Game, SquadRequest, CustomUser
from .serializers import (
    SerializadorJuego, 
    SerializadorSquad, 
    SerializadorRegistro
)

# 1. REGISTRO DE USUARIOS 
class VistaRegistro(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [] 
    
    def post(self, request):
        serializer = SerializadorRegistro(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2. LISTA DE JUEGOS 
class VistaListaJuegos(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [] 
    
    def get(self, request):
        juegos = Game.objects.all()
        serializer = SerializadorJuego(juegos, many=True)
        return Response(serializer.data)

#  3. SQUADS (Protegido con JWT) 
class VistaSquads(APIView):
    # Forzamos JWT para evitar error CSRF si hay sesión de admin abierta
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Listar ordenada por fecha mas reciente
        squads = SquadRequest.objects.all().order_by('-fecha_creacion')
        
        # Filtro opcional por URL: juego=valorant
        slug = request.query_params.get('juego')
        if slug:
            squads = squads.filter(juego__slug=slug)
            
        serializer = SerializadorSquad(squads, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SerializadorSquad(data=request.data)
        if serializer.is_valid():
            # Guardamos asignando automáticamente al usuario del token
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 4. DETALLE DE SQUAD 
class VistaDetalleSquad(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            squad = SquadRequest.objects.get(pk=pk)
        except SquadRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Validación donde Solo el dueño puede borrar
        if squad.usuario != request.user:
            return Response({"error": "No tienes permiso para borrar este squad."}, status=status.HTTP_403_FORBIDDEN)
            
        squad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#  5. ESTADÍSTICAS (Para Gráficos del Dashboard)
class VistaEstadisticas(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [] 

    def get(self, request):
        #  Contadores Totales
        total_usuarios = CustomUser.objects.count()
        total_squads = SquadRequest.objects.count()
        
        # Reporte Diario 
        hoy = timezone.now().date()
        squads_hoy = SquadRequest.objects.filter(fecha_creacion__date=hoy).count()

        #  Datos para el Gráfico 
        
        squads_por_juego = SquadRequest.objects.values('juego__nombre').annotate(total=Count('id'))

        data = {
            "usuarios": total_usuarios,
            "squads_total": total_squads,
            "squads_hoy": squads_hoy,
            "grafico": list(squads_por_juego)
        }
        return Response(data)