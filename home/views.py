from rest_framework import generics, permissions
from .models import Department, Patient, Doctor, PatientRecord
from .serializers import DepartmentSerializer, PatientSerializer, DoctorSerializer, PatientRecordSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import HttpResponse




class CustomTokenObtainPairView(TokenObtainPairView):
    # Customize token response if needed
    pass

class CustomTokenRefreshView(TokenRefreshView):
    # Customize token response if needed
    pass

class IsDoctorOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or hasattr(request.user, 'doctor')

class IsPatientOrDoctor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if hasattr(request.user, 'patient'):
            return obj.patient.user == request.user or (hasattr(request.user, 'doctor') and obj.department == request.user.doctor.department)
        return False

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

    def get_queryset(self):
        if self.request.user.is_superuser:
            return PatientRecord.objects.all()
        if hasattr(self.request.user, 'doctor'):
            return PatientRecord.objects.filter(department=self.request.user.doctor.department)
        return PatientRecord.objects.none()

    def perform_create(self, serializer):
        serializer.save(department=self.request.user.doctor.department)

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
    return HttpResponse("Welcome to the grey scientific labs")
