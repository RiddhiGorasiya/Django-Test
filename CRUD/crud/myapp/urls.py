from django.urls import path
from myapp import views

urlpatterns = [
    path('create/', views.StudentCreateView.as_view(), name='create'),
    path('', views.StudentListView.as_view(), name='list'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', views.StudentUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.StudentDeleteView.as_view(), name='delete'),
]
