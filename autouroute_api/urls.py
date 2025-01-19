from django.urls import path
from . import views
from .views import TollListCreateView, TollRetrieveUpdateDestroyView
from .views import create_checkout_session
from .views import payment_success

urlpatterns = [
    # Authentication
    path('api/login/', views.user_login, name='user_login'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),

    # Highways
    path('api/highways/', views.HighwayListView.as_view(), name='highway-list'),
    path('api/highways/<int:pk>/', views.HighwayDetailView.as_view(), name='highway-detail'),
    path('api/status/', views.HighwayStatusListView.as_view(), name='highway-status-list'),
    path('api/status/<int:pk>/', views.HighwayStatusDetailView.as_view(), name='highway-status-detail'),

    # Accidents
    path('api/accidents/', views.AccidentListView.as_view(), name='accident-list'),
    path('api/accidents/<int:pk>/', views.AccidentDetailView.as_view(), name='accident-detail'),

    # Tolls
    path('api/tolls/', views.TollListView.as_view(), name='toll-list'),
    path('api/tolls/<int:pk>/', views.TollDetailView.as_view(), name='toll-detail'),
    path('api/tolls/highway/<int:id>/', views.HighwayTollListView.as_view(), name='highway-toll-list'),
    path('tolls/', TollListCreateView.as_view(), name='toll-list-create'),
    path('tolls/<int:pk>/', TollRetrieveUpdateDestroyView.as_view(), name='toll-retrieve-update-destroy'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),


    # Emergency Contacts
    path('api/emergencycontacts/', views.EmergencyContactListView.as_view(), name='emergency-contact-list'),
    path('api/emergencycontacts/highway/<int:id>/', views.HighwayEmergencyContactListView.as_view(), name='highway-emergency-contact-list'),

    # Rest Areas
    path('api/restareas/', views.RestAreaListView.as_view(), name='rest-area-list'),
    path('api/restareas/<int:pk>/', views.RestAreaDetailView.as_view(), name='rest-area-detail'),
    path('api/restareas/highway/<int:id>/', views.HighwayRestAreaListView.as_view(), name='highway-rest-area-list'),

    # Template Views (no API prefix)
    path('login/', views.login_view, name='login_view'),  # For the template login page
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('frontend/', views.frontend_dashboard_view, name='frontend_index'),
    path('logout/', views.user_logout, name='user_logout'),
    path('googlemaps/', views.googlemaps, name='googlemaps'),
    path('success/', payment_success, name='payment_success'),
    
    path('', views.login_view, name='index'), 
]