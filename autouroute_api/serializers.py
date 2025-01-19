from rest_framework import serializers
from .models import HighwayStatus, User, Accident, Toll, EmergencyContact, RestArea, Highway

class UserSerializer(serializers.ModelSerializer):
  class Meta:
      model = User
      fields = ['id', 'username', 'role']

class AccidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accident
        fields = '__all__'

class HighwayStatusSerializer(serializers.ModelSerializer):
  class Meta:
    model = HighwayStatus
    fields = '__all__'


class HighwaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Highway
        fields = ['id', 'name', 'description']  

class TollSerializer(serializers.ModelSerializer):
    highway = HighwaySerializer(read_only=True) 

    class Meta:
        model = Toll
        fields = '__all__'



class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'

class RestAreaSerializer(serializers.ModelSerializer):
  class Meta:
      model = RestArea
      fields = '__all__'