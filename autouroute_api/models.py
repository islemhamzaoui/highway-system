from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

class Highway(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    coordinates = models.JSONField(blank=True, null=True)  
    def __str__(self):
        return self.name
    


class Accident(models.Model):
    ACCIDENT_TYPES = [
        ('collision', 'Collision'),
        ('rollover', 'Rollover'),
        ('pedestrian', 'Pedestrian Accident'),
        ('other', 'Other'),
    ]
    SEVERITY_LEVELS = [
        ('minor', 'Minor'),
        ('major', 'Major'),
        ('fatal', 'Fatal'),
    ]
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('under_investigation', 'Under Investigation'),
        ('resolved', 'Resolved'),
    ]

    highway = models.ForeignKey(Highway, on_delete=models.CASCADE, related_name='accidents')
    accident_type = models.CharField(max_length=50, choices=ACCIDENT_TYPES)
    severity = models.CharField(max_length=50, choices=SEVERITY_LEVELS)
    description = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reported_at = models.DateTimeField(auto_now_add=True)
    emergency_contact_called = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='reported')

    def __str__(self):
        return f"Accident on {self.highway.name} ({self.accident_type})"

class HighwayStatus(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('under_construction', 'Under Construction'),
        ('closed', 'Closed'),
    ]

    highway = models.ForeignKey(Highway, on_delete=models.CASCADE, related_name='status_updates')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.highway.name} - {self.status}"

class EmergencyContact(models.Model):
    CONTACT_TYPES = [
        ('police', 'Police'),
        ('ambulance', 'Ambulance'),
        ('fire', 'Fire Department'),
    ]

    highway = models.ForeignKey(Highway, on_delete=models.CASCADE, related_name='emergency_contacts')
    contact_type = models.CharField(max_length=50, choices=CONTACT_TYPES)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.contact_type} - {self.location}"

class Toll(models.Model):
    VEHICLE_CATEGORIES = [
        ('car', 'Car'),
        ('truck', 'Truck'),
        ('motorcycle', 'Motorcycle'),
    ]

    highway = models.ForeignKey(Highway, on_delete=models.CASCADE, related_name='tolls')
    location = models.CharField(max_length=255)
    vehicle_category = models.CharField(max_length=50, choices=VEHICLE_CATEGORIES)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  

    def __str__(self):
        return f"Toll at {self.location} ({self.vehicle_category})"



class RestArea(models.Model):
    highway = models.ForeignKey(Highway, on_delete=models.CASCADE, related_name='rest_areas')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    has_gas_station = models.BooleanField(default=False)
    has_restaurant = models.BooleanField(default=False)
    has_bathroom = models.BooleanField(default=False)

    def __str__(self):
        return f"Rest Area: {self.name} on {self.highway.name}"
    

