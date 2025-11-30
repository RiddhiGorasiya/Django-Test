from django.urls import path
from . import views 

urlpatterns = [
    # path('', views.ApiOverview, name='home'),
    path("register/", views.register_user, name='register'),
    path("login/", views.login_user, name='login'),
    path("items/", views.view_items, name='view_items'),            # GET
    path("items/add/", views.add_items, name='add-items'),         # POST
    path("items/<int:pk>/update/", views.update_items, name='update-items'),  # PUT
    path("items/<int:pk>/delete/", views.delete_items, name='delete-items'),  # DELETE
]

# urlpatterns = [
#     path('', views.ApiOverview, name='home'),
#     path('create/', views.add_items, name='add-items'),
#     path('all/', views.view_items, name='view_items'),
#     path('update/<int:pk>/', views.update_items, name='update-items'),
#     path('item/<int:pk>/delete/', views.delete_items, name='delete-items'),
# ]