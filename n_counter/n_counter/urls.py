from django.contrib import admin
from django.urls import path
from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('delete/<int:id>/', views.delete_consume, name="delete"),
    path('chart-data/', views.nutrient_data, name="chart-data"),
    path('set-goal/', views.set_health_goal, name="set-goal"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("add-food/", views.add_food, name="add-food"),
]