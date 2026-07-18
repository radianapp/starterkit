from django.contrib import admin
from .models import Activity, SystemUpdate

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'description')

@admin.register(SystemUpdate)
class SystemUpdateAdmin(admin.ModelAdmin):
    list_display = ('version', 'title', 'update_type', 'release_date')
    list_filter = ('update_type', 'release_date')
    search_fields = ('version', 'title', 'description')
