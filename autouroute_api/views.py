from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout
from django.middleware.csrf import get_token
from django.http import JsonResponse
from .models import HighwayStatus, User, Accident, Toll, EmergencyContact, RestArea
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Highway
import json

from .serializers import (
    HighwayStatusSerializer,
    AccidentSerializer,
    TollSerializer,
    EmergencyContactSerializer,
    RestAreaSerializer
)
from rest_framework_simplejwt.authentication import JWTAuthentication 
from django.middleware.csrf import get_token
import stripe
from django.conf import settings
from django.shortcuts import render
print("Stripe Secret Key:", settings.STRIPE_SECRET_KEY) 
stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
        },
         required=['username','password']
),
    responses={
        200: openapi.Response(description="Logged in successfully"),
        401: openapi.Response(description="Invalid credentials"),
        400: openapi.Response(description="Invalid request")
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
     if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
              return Response({'message': 'Missing username or password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            serializer = TokenObtainPairSerializer(data={'username':username, 'password': password})
            if serializer.is_valid():
               token = serializer.validated_data
               return Response({'message': 'Logged in', 'token': token}, status=status.HTTP_200_OK)
            else:
               return Response({'message':'Invalid credentials'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
     return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)



class HighwayListView(generics.ListAPIView):
    queryset = HighwayStatus.objects.all()
    serializer_class = HighwayStatusSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

class HighwayDetailView(generics.RetrieveAPIView):
    queryset = HighwayStatus.objects.all()
    serializer_class = HighwayStatusSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

class HighwayStatusListView(generics.ListAPIView):
    queryset = HighwayStatus.objects.all()
    serializer_class = HighwayStatusSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

class HighwayStatusDetailView(generics.RetrieveAPIView):
    queryset = HighwayStatus.objects.all()
    serializer_class = HighwayStatusSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]



from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

class AccidentListView(generics.ListCreateAPIView):
    queryset = Accident.objects.all()
    serializer_class = AccidentSerializer
    authentication_classes = [] 
    permission_classes = []     
    parser_classes = [MultiPartParser, FormParser]  

    def create(self, request, *args, **kwargs):
        print("Request Data:", request.data)  
        data = {
            'highway': request.data.get('highway'),
            'accident_type': request.data.get('accident_type'),
            'severity': request.data.get('severity'),
            'description': request.data.get('description'),
            'emergency_contact_called': request.data.get('emergency_contact_called') == 'on',
        }

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer Errors:", serializer.errors)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Accident.objects.all()
    serializer_class = AccidentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()
    
    def perform_destroy(self, instance):
        instance.delete()


class TollListView(generics.ListCreateAPIView):
    queryset = Toll.objects.all()
    serializer_class = TollSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
      user = get_object_or_404(User, pk=self.request.user.id)
      if user.role != 'authority':
          raise Exception("You are not allowed to perform this action")
      serializer.save(highway_id=self.request.data.get('highway'), user=user)

class TollDetailView(generics.RetrieveAPIView):
    queryset = Toll.objects.all()
    serializer_class = TollSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

class HighwayTollListView(generics.ListAPIView):
    serializer_class = TollSerializer
    authentication_classes = [JWTAuthentication] 

    def get_queryset(self):
        highway_id = self.kwargs['id']
        get_object_or_404(HighwayStatus, id = highway_id)
        return Toll.objects.filter(highway_id=highway_id)

class TollListCreateView(generics.ListCreateAPIView):
    queryset = Toll.objects.all()
    serializer_class = TollSerializer

class TollRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Toll.objects.all()
    serializer_class = TollSerializer
    
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = data.get('amount')  
            currency = data.get('currency', 'usd') 
            # Create a Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency,
                        'product_data': {
                            'name': 'Toll Payment',
                        },
                        'unit_amount': amount,  
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:8001/success/',  
                cancel_url='http://localhost:8001/cancel/',  
            )

            return JsonResponse({
                'sessionId': session.id,
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)




class EmergencyContactListView(generics.ListAPIView):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

class HighwayEmergencyContactListView(generics.ListAPIView):
    serializer_class = EmergencyContactSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
         highway_id = self.kwargs['id']
         get_object_or_404(HighwayStatus, id = highway_id)
         return EmergencyContact.objects.filter(highway_id=highway_id)



class RestAreaListView(generics.ListAPIView):
    queryset = RestArea.objects.all()
    serializer_class = RestAreaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class RestAreaDetailView(generics.RetrieveAPIView):
    queryset = RestArea.objects.all()
    serializer_class = RestAreaSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]


class HighwayRestAreaListView(generics.ListAPIView):
    serializer_class = RestAreaSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        highway_id = self.kwargs['id']
        get_object_or_404(HighwayStatus, id = highway_id)
        return RestArea.objects.filter(highway_id=highway_id)


from django.db.models import OuterRef, Subquery

from django.shortcuts import render
from django.db.models import OuterRef, Subquery
from .models import Highway, HighwayStatus, Accident, Toll, EmergencyContact, RestArea

def dashboard_view(request):
    
    context = {
        'pk_test_51QiYbvBXMMkPWU9DyR5zfOeJ1W83GBInB05JRheYinz842Bz95ZpyVExHKkLrtkUMqKKp38JD2d4wz5tZoPEHFtH00tL7ptyMo': settings.STRIPE_PUBLISHABLE_KEY,
    }
    
    latest_status_subquery = HighwayStatus.objects.filter(
        highway=OuterRef('pk')
    ).order_by('-updated_at').values('status')[:1]

  
    highways = Highway.objects.annotate(
        latest_status=Subquery(latest_status_subquery)
    ).values('id', 'name', 'coordinates', 'latest_status')

    
    accidents = Accident.objects.all()

   
    tolls = Toll.objects.all()
    emergency_contacts = EmergencyContact.objects.all()
    rest_areas = RestArea.objects.all()

  
    context = {
        'accidents': accidents,
        'highways': list(highways),
        'tolls': tolls,
        'emergency_contacts': emergency_contacts,
        'rest_areas': rest_areas,
    }

    return render(request, 'dashboard.html', context)
   
def frontend_dashboard_view(request):
    return render(request, 'dashboard.html')

def user_logout(request):
    logout(request)
    return redirect('/login/')

def googlemaps(request):
    return render(request, 'googlemaps.html')

def index(request):
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'login.html')

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Toll

@csrf_exempt
def payment_success(request):
    return render(request, 'payment_success.html')