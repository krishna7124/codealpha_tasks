from django.contrib import admin
from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('logout/', views.custom_logout, name="logout"),
    path('pdf/', views.pdf, name='pdf'),
    path('admin/', admin.site.urls),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('', views.expenses, name='expenses'),
    path('update_expense/<id>', views.update_expense, name='update_expense'),
    path('delete_expense/<id>', views.delete_expense, name='delete_expense'),
]
