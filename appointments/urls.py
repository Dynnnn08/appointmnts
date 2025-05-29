from django.urls import path
from .views import RegisterAPI, LoginAPI, BookAppointmentAPI, ListAppointmentsAPI, LogoutAPI
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('registerAPI/', RegisterAPI.as_view()),
    path('loginAPI/', LoginAPI.as_view()),
    path('appointments/book/', BookAppointmentAPI.as_view()),
    path('appointmentsAPI/', ListAppointmentsAPI.as_view()),
    path('api-token-auth/', obtain_auth_token),

    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('book/', views.book_appointment, name='book'),
    path('appointments/', views.list_appointments, name='appointments'),
    path('logoutAPI/', LogoutAPI.as_view(), name='api_logout'),
]
