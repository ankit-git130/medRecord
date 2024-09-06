from rest_framework import generics, permissions
from .models import Department, Patient, Doctor, PatientRecord
from .serializers import DepartmentSerializer, PatientSerializer, DoctorSerializer, PatientRecordSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse

# Custom permissions
class IsDoctorOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or hasattr(request.user, 'doctor')

class IsPatientOrDoctor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'patient'):
            return obj.patient.user == request.user
        if hasattr(request.user, 'doctor'):
            return obj.patient.department == request.user.doctor.department
        return False

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user-dashboard')  # Redirect to user dashboard after login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# User Dashboard View
class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Determine if the user is a patient or a doctor
        if hasattr(request.user, 'patient'):
            patient = Patient.objects.get(user=request.user)
            data = {
                'role': 'Patient',
                'username': patient.user.username,
                'department': patient.department.name
            }
        elif hasattr(request.user, 'doctor'):
            doctor = Doctor.objects.get(user=request.user)
            data = {
                'role': 'Doctor',
                'username': doctor.user.username,
                'department': doctor.department.name
            }
        else:
            data = {
                'message': 'No associated role found'
            }
        return Response(data)

# Views
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

class CustomTokenRefreshView(TokenRefreshView):
    pass

class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]

class DepartmentDetailView(generics.RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]

class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsDoctorOrSuperuser]

class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsDoctorOrSuperuser]

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsPatientOrDoctor]

class PatientRecordListCreateView(generics.ListCreateAPIView):
    queryset = PatientRecord.objects.all()
    serializer_class = PatientRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return PatientRecord.objects.all()
        elif hasattr(user, 'doctor'):
            return PatientRecord.objects.filter(patient__department=user.doctor.department)
        elif hasattr(user, 'patient'):
            return PatientRecord.objects.filter(patient=user.patient)
        return PatientRecord.objects.none()

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'doctor'):
            serializer.save(department=self.request.user.doctor.department)
        else:
            serializer.save()

class PatientRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PatientRecord.objects.all()
    serializer_class = PatientRecordSerializer
    permission_classes = [IsPatientOrDoctor]

class DepartmentDoctorsView(generics.ListAPIView):
    serializer_class = DoctorSerializer

    def get_queryset(self):
        department_id = self.kwargs['pk']
        return Doctor.objects.filter(department_id=department_id)

class DepartmentPatientsView(generics.ListAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        department_id = self.kwargs['pk']
        return Patient.objects.filter(department_id=department_id)

def home(request):
    return HttpResponse("Welcome to the Grey Scientific Labs")
