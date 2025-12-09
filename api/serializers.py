from rest_framework import serializers
from .models import CustomUser, Game, SquadRequest

# 1. REGISTRO
class SerializadorRegistro(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'gamertag']

    def create(self, datos):
        return CustomUser.objects.create_user(**datos)

# 2. JUEGOS
class SerializadorJuego(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"

# 3. SQUADS
class SerializadorSquad(serializers.ModelSerializer):
    gamertag_creador = serializers.ReadOnlyField(source='usuario.gamertag')
    # CAMPO CLAVE: Permite al frontend saber si soy el dueño (comparando username)
    username_creador = serializers.ReadOnlyField(source='usuario.username')
    
    nombre_juego = serializers.ReadOnlyField(source='juego.nombre')
    slug_juego = serializers.ReadOnlyField(source='juego.slug')
    
    id_juego_seleccionado = serializers.PrimaryKeyRelatedField(
        queryset=Game.objects.all(), source='juego', write_only=True
    )

    class Meta:
        model = SquadRequest
        fields = ['id', 'gamertag_creador', 'username_creador', 'nombre_juego', 
                  'slug_juego', 'id_juego_seleccionado', 'rango_requerido', 
                  'usa_microfono', 'descripcion', 'fecha_creacion']
        read_only_fields = ['usuario', 'fecha_creacion']

    def validate_descripcion(self, valor):
        if len(valor) < 10:
            raise serializers.ValidationError("Mínimo 10 caracteres.")
        return valor