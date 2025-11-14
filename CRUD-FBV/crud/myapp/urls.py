from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('show/', views.add_show, name="addandshow"),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('delete/<int:id>', views.delete_data, name="deletedata"),
    path('update/<int:id>', views.update_data, name="updatedata"),
    path('image-upload/', views.image_view, name='image_upload'),
    # path('pm-dashboard/', views.pm_dashboard, name='pm_dashboard'),
]