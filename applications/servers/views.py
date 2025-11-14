from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.contrib.auth import login, authenticate # type: ignore

from .models import Server
from .forms import ServerCreateForm
from .services.docker_manager import DockerManager
import requests # type: ignore
from django.contrib.auth import logout as auth_logout # type: ignore
from django.conf import settings # type: ignore
from django.shortcuts import reverse # type: ignore

@login_required
def dashboard(request):
    servers = Server.objects.filter(owner=request.user)
    
    try:
        public_ip = requests.get('https://api.ipify.org').text
    except:
        public_ip = "localhost"
    return render(request, 'servers/dashboard.html', {'servers': servers, 'public_ip': public_ip})

@login_required
def create_server(request):
    if request.method == 'POST':
        form = ServerCreateForm(request.POST)
        if form.is_valid():
            server = form.save(commit=False)
            server.owner = request.user
            server.save()

            # Try to create docker container
            try:
                dm = DockerManager()
                # default container internal port for Minecraft is 25565 unless otherwise
                internal_port = 25565
                host_port = server.port or 25565
                cid = dm.create_container(image=server.image, name=f"srv-{server.id}", ram=server.ram, cpu=server.cpu, host_port=host_port, container_port=internal_port)
                if cid:
                    server.container_id = cid
                    server.status = 'running'
                    server.port = host_port
                    server.save()
                    messages.success(request, 'Server creado y contenedor iniciado')
                else:
                    messages.warning(request, 'Server creado pero no se pudo iniciar el contenedor')
            except PermissionError as e:
                messages.warning(request, f'Server creado pero Docker no disponible (permiso): {e}')
            except Exception as e:
                msg = str(e)
                if 'port' in msg and 'already' in msg:
                    messages.error(request, f'No se pudo iniciar el contenedor: el puerto {server.port} ya está en uso en el host.')
                else:
                    messages.warning(request, f'Server creado pero Docker no disponible: {e}')

            return redirect('servers:dashboard')
    else:
        form = ServerCreateForm()
    return render(request, 'servers/create.html', {'form': form})


@login_required
def start_server(request, pk):
    server = get_object_or_404(Server, pk=pk, owner=request.user)
    if server.container_id:
        dm = DockerManager()
        if dm.start_container(server.container_id):
            server.status = 'running'
            server.save()
            messages.success(request, 'Servidor iniciado')
        else:
            messages.error(request, 'No fue posible iniciar el servidor')
    return redirect('servers:dashboard')


@login_required
def stop_server(request, pk):
    server = get_object_or_404(Server, pk=pk, owner=request.user)
    if server.container_id:
        dm = DockerManager()
        if dm.stop_container(server.container_id):
            server.status = 'stopped'
            server.save()
            messages.success(request, 'Servidor detenido')
        else:
            messages.error(request, 'No fue posible detener el servidor')
    return redirect('servers:dashboard')


@login_required
def delete_server(request, pk):
    server = get_object_or_404(Server, pk=pk, owner=request.user)
    if server.container_id:
        dm = DockerManager()
        dm.remove_container(server.container_id)
    server.delete()
    messages.success(request, 'Servidor eliminado')
    return redirect('servers:dashboard')


def signup(request):
    """Registro público de usuarios usando UserCreationForm.
    Al registrarse, el usuario queda autenticado automáticamente y redirige al dashboard.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Autenticar y loguear al usuario
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
            messages.success(request, 'Registro completado. Bienvenido!')
            return redirect('servers:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def logout_view(request):
    """Logout view that accepts GET or POST and redirects to LOGOUT_REDIRECT_URL."""
    # support both POST and GET for convenience
    auth_logout(request)
    redirect_to = getattr(settings, 'LOGOUT_REDIRECT_URL', None) or '/accounts/login/'
    return redirect(redirect_to)
