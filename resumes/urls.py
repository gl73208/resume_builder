from django.urls import path, include
from . import views
from resumes.views import home
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='resumes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('my-resumes/', views.my_resumes, name='my_resumes'),
    path('resume/new/', views.resume_create, name='resume_create'),
    path('resume/<int:pk>/', views.resume_detail, name='resume_detail'),
    path('resume/<int:pk>/edit/', views.resume_edit, name='resume_edit'),
    path('resume/<int:pk>/delete/', views.resume_delete, name='resume_delete'),
    path('resume/<int:pk>/export-pdf/', views.resume_export_pdf, name='resume_export_pdf'),
]

