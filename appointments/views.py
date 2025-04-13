from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate

from .models import Appointment
from .serializers import RegisterSerializer, AppointmentSerializer

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages

API_URL = 'http://localhost:8000/api'

def home(request):
    if request.user.is_authenticated:
        token, created = Token.objects.get_or_create(user=request.user)
        response = requests.get(
            f'{API_URL}/appointmentsAPI/',
            headers={'Authorization': f'Token {token.key}'}
        )
        appointments = Appointment.objects.filter(user=request.user)
        if response.status_code == 200:
            appointments = response.json()
        else:
            appointments = []
    else:
        appointments = []

    return render(request, 'home.html', {'appointments': appointments})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        response = requests.post(
            f'{API_URL}/registerAPI/',
            json={
                'username': username,
                'password': password,
                'email': email,
            }
        )
        if response.status_code == 201:
            messages.success(request, 'User Created Successfully!')
            return redirect('/register/')
        elif response.status_code == 400:
            # Handle bad request (400)
            messages.error(request, 'Invalid credentials or request format. Please try again.')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        response = requests.post(
            f'{API_URL}/loginAPI/',
            json={'username': username, 'password': password}
        )
        if response.status_code == 200:
            token = response.json().get('token')

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/?authToken=' + token)
        elif response.status_code == 400:
            # Handle bad request (400)
            messages.error(request, 'Invalid credentials or request format. Please try again.')
        else:  
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

@login_required
def book_appointment(request):
    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time']
        service = request.POST['service']

        token, created = Token.objects.get_or_create(user=request.user)

        response = requests.post(f'{API_URL}/appointments/book/', json={
            'date': date,
            'time': time,
            'service': service
        }, headers={'Authorization': f'Token {token.key}'})

        if response.status_code == 201:
            messages.success(request, 'Appointment booked successfully!')
        else:
            messages.error(request, f'Failed to book appointment: {response.text}')

    return render(request, 'book.html')

@login_required
def list_appointments(request):
    token, created = Token.objects.get_or_create(user=request.user)
    response = requests.get(f'{API_URL}/appointmentsAPI/', headers={'Authorization': f'Token {token.key}'})

    if response.status_code == 200:
        appointments = response.json()
    else:
        appointments = []

    return render(request, 'appointments.html', {'appointments': appointments})

# API Starts Here
class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)

class BookAppointmentAPI(generics.CreateAPIView):
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ListAppointmentsAPI(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)