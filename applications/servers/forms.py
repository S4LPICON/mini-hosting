from django import forms # type: ignore
from .models import Server


IMAGE_CHOICES = (
    ('itzg/minecraft-server:latest', 'Minecraft Java (latest)'),
    ('itzg/minecraft-server:java16', 'Minecraft Java (Java 16)'),
    ('ubuntu:22.04', 'Ubuntu 22.04 (generic)'),
)


class ServerCreateForm(forms.ModelForm):
    image = forms.ChoiceField(choices=IMAGE_CHOICES)
    port = forms.IntegerField(initial=25565, min_value=1, max_value=65535, help_text='Host port to map to the container (default Minecraft: 25565)')

    class Meta:
        model = Server
        fields = ('name', 'image', 'ram', 'cpu', 'storage', 'port')
