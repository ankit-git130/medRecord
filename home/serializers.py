from rest_framework import serializers
from .models import Department, Patient, Doctor, PatientRecord

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'diagnostics', 'location', 'specialization']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['user', 'department']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['user', 'department']

class PatientRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRecord
        fields = ['record_id', 'patient', 'created_date', 'diagnostics', 'observations', 'treatments', 'department', 'misc']
