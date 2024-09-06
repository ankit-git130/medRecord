from django.urls import path
from .views import (
    home,
    DepartmentListCreateView, DepartmentDetailView,
    DoctorListCreateView, DoctorDetailView,
    PatientListCreateView, PatientDetailView,
    PatientRecordListCreateView, PatientRecordDetailView,
    DepartmentDoctorsView, DepartmentPatientsView,
    CustomTokenObtainPairView, CustomTokenRefreshView,
    login_view, UserDashboardView
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('user-dashboard/', UserDashboardView.as_view(), name='user-dashboard'),
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentDetailView.as_view(), name='department-detail'),
    path('departments/<int:pk>/doctors/', DepartmentDoctorsView.as_view(), name='department-doctors'),
    path('departments/<int:pk>/patients/', DepartmentPatientsView.as_view(), name='department-patients'),
    path('doctors/', DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('patients/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('patient_records/', PatientRecordListCreateView.as_view(), name='patient-record-list-create'),
    path('patient_records/<int:pk>/', PatientRecordDetailView.as_view(), name='patient-record-detail'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
