from django.db import models # type: ignore
from django.contrib.auth import get_user_model # type: ignore

User = get_user_model()


class Server(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servers')
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=200, default='ubuntu:22.04')
    ram = models.IntegerField(help_text='RAM in MB', default=1024)
    cpu = models.FloatField(help_text='CPU cores', default=1.0)
    storage = models.IntegerField(help_text='Storage in MB', default=10240)
    container_id = models.CharField(max_length=128, blank=True, null=True)
    port = models.IntegerField(help_text='Host port', default=25565)
    status = models.CharField(max_length=20, choices=(('stopped', 'Stopped'), ('running', 'Running')), default='stopped')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.owner})"
