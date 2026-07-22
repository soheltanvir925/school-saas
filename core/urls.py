from django.urls import path
from .views import IndexView, RegisterSchoolView, DashboardView

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register-school/', RegisterSchoolView.as_view(), name='register_school'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
