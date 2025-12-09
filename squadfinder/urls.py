from django.contrib import admin
from django.urls import path, include
from .views import LoginView, RegistroView, DashboardView, StatsView

urlpatterns = [
  
    path('admin/', admin.site.urls),

    # Conexión con API
    path('api/', include('api.urls')),

    # Vistas del Frontend (Nuevas con diseño modernizado)
    path('', LoginView.as_view(), name='login'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('stats/', StatsView.as_view(), name='stats'),
]
