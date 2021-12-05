from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('Singup/', views.Singup, name='Singup'),
    path('Login/', views.Login, name='Login'),
    path('Logout/', views.Logout, name="Logout"),
    path('deleteAccount/', views.deleteAccount, name="deleteAccount"),
    path('Dashboard/', views.Dashboard, name="Dashboard"),
    path('Search/', views.Search, name="Search"),
    path('EditProfile/', views.EditProfile, name="EditProfile"),
    path('viewHomeProject/<int:pk>/', views.viewHomeProject, name="viewHomeProject"),
    path('Projects/', views.Projects, name="Projects"),
    path('AddProject/', views.AddProject, name="AddProject"),
    path('EditProject/<int:pk>/', views.EditProject, name="EditProject"),
    path('DeleteProject/<int:pk>/', views.DeleteProject, name="DeleteProject"),
    path('DasViewProject/<int:pk>/', views.bashboardViewProject, name="DasViewProject"),
    path('forgetPassword/', views.forgetPassword, name="forgetPassword")
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)