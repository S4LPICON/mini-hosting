from django.urls import path
from . import views

app_name = 'servers'

urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'),
    path('servers/', views.dashboard, name='dashboard'),
    path('servers/create/', views.create_server, name='create'),
    path('servers/<int:pk>/start/', views.start_server, name='start'),
    path('servers/<int:pk>/stop/', views.stop_server, name='stop'),
    path('servers/<int:pk>/delete/', views.delete_server, name='delete'),
    # set root to dashboard for convenience
    path('', views.dashboard, name='root_dashboard'),
]
