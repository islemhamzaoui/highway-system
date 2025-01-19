from django.contrib import admin
from .models import Highway, Accident, HighwayStatus, EmergencyContact, Toll, RestArea

@admin.register(Highway)
class HighwayAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Accident)
class AccidentAdmin(admin.ModelAdmin):
    list_display = ('highway', 'accident_type', 'severity', 'reported_at', 'status')
    list_filter = ('accident_type', 'severity', 'status')
    search_fields = ('highway__name', 'description')

@admin.register(HighwayStatus)
class HighwayStatusAdmin(admin.ModelAdmin):
    list_display = ('highway', 'status', 'start_date', 'end_date')
    list_filter = ('status',)
    search_fields = ('highway__name', 'description')

@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('highway', 'contact_type', 'phone_number', 'location')
    list_filter = ('contact_type',)
    search_fields = ('highway__name', 'location')

@admin.register(Toll)
class TollAdmin(admin.ModelAdmin):
    list_display = ('highway', 'location', 'vehicle_category', 'rate', 'paid', 'payment_id', 'created_at', 'user')
    list_filter = ('vehicle_category', 'paid')
    search_fields = ('highway__name', 'location', 'payment_id')
    readonly_fields = ('created_at',)  # Make created_at read-only



@admin.register(RestArea)
class RestAreaAdmin(admin.ModelAdmin):
    list_display = ('highway', 'name', 'location', 'has_gas_station', 'has_restaurant', 'has_bathroom')
    list_filter = ('has_gas_station', 'has_restaurant', 'has_bathroom')
    search_fields = ('highway__name', 'name', 'location')