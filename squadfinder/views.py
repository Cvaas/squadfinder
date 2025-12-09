from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = 'login.html'

class RegistroView(TemplateView):
    template_name = 'registro.html'

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

class StatsView(TemplateView):
    template_name = 'stats.html'
