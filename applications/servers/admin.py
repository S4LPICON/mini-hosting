from django.contrib import admin # type: ignore
from .models import Server


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'image', 'ram', 'cpu', 'storage', 'port', 'created_at')
    list_filter = ('status', 'image')
    search_fields = ('name', 'owner__username')
