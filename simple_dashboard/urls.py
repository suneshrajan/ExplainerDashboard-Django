from django.urls import path
from simple_dashboard import views as sd_views

urlpatterns = [
    path('start-dashboard', sd_views.show_dashboard, name='Display Dashboard'),
    path('stop-dashboard', sd_views.stop_dashboard, name='Hide Dashboard')
]