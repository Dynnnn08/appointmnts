# appointments/admin.py
from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'status', 'created_at')
    list_filter = ('status', 'date')
    list_editable = ('status',)  # Allows direct editing in list view
    search_fields = ['user__username']
    actions = ['approve_selected', 'decline_selected', 'mark_done']
    
    def approve_selected(self, request, queryset):
        queryset.update(status='ACCEPTED')
    approve_selected.short_description = "Mark selected as ACCEPTED"
    
    def decline_selected(self, request, queryset):
        queryset.update(status='DECLINED')
    decline_selected.short_description = "Mark selected as DECLINED"
    
    def mark_done(self, request, queryset):
        queryset.update(status='DONE')
    mark_done.short_description = "Mark selected as DONE"