from django.contrib import admin
from .models import CustomUser, Game, SquadRequest


admin.site.register(CustomUser)
admin.site.register(Game)
admin.site.register(SquadRequest)