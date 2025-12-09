#!/usr/bin/env python
# Script para agregar juegos de ejemplo a SquadFinder

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'squadfinder.settings')
django.setup()

from api.models import Game

juegos = [
    {"nombre": "Valorant", "slug": "valorant"},
    {"nombre": "League of Legends", "slug": "lol"},
    {"nombre": "Counter-Strike 2", "slug": "cs2"},
    {"nombre": "Apex Legends", "slug": "apex"},
    {"nombre": "Fortnite", "slug": "fortnite"},
    {"nombre": "Overwatch 2", "slug": "overwatch2"},
]

print("Agregando juegos de ejemplo...")
for juego in juegos:
    obj, created = Game.objects.get_or_create(
        slug=juego["slug"],
        defaults={"nombre": juego["nombre"]}
    )
    if created:
        print(f"✅ Creado: {juego['nombre']}")
    else:
        print(f"ℹ️  Ya existe: {juego['nombre']}")

print("\n¡Juegos agregados exitosamente!")
