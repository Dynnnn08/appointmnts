from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
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
    return render(request, 'home.html')


def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('book')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

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
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ListAppointmentsAPI(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)
