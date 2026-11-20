from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('questions/', views.questions_list_view, name='questions_list'),
    path('add-question/', views.add_question_view, name='add_question'),
    path('exams/', views.exam_list_view, name='exam_list'),
    path('exam/<int:exam_id>/start/', views.exam_page_view, name='exam_page'),
    path('exam/<int:attempt_id>/submit/', views.submit_exam_view, name='submit_exam'),
    path('result/<int:attempt_id>/', views.result_view, name='result'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('certificates/', views.certificate_list_view, name='certificates'),
    path('certificate/<int:attempt_id>/', views.view_certificate, name='view_certificate'),
    
]
