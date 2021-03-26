from django.urls import include, path

from .views import * 
app_name = 'Web'
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("home", IndexView.as_view(),name="home" ),
    path("", LoginView.as_view(),name="login" ),
    path('logout/',LogoutView.as_view(next_page="/"),name="logout"),
    path('users/',UserListView.as_view(),name="usuarios"),

    path("users/create/",UsuarioCreateView.as_view(),name="create_user"),
    path("users/edit/<int:pk>/",UsuarioUpdateView.as_view(),name="edit_user"),
    path('Usuario/changepassword/<int:pk>/', UsuarioUpdatePasswordView.as_view(), name='UsuarioChangePassword'),
    path('Usuario/reset/<int:pk>/', UsuarioResetPasswordView, name='UsuarioResetPassword'),
    path('Usuario/activate/<int:pk>/', UsuarioActivate, name='UsuarioActivate   '),
    path('Usuario/desactivate/<int:pk>/', UsuarioDesactivate, name='UsuarioDesactivate'),
    path('import/', run, name='inportEESS'),
    path('EESS/', EstablecimientoListView.as_view() ,name='establecimientos'),
    path('programacion/', ProgramacionListView.as_view() ,name='programaciones'),
    path('liquidacion/', LiquidacionListView.as_view() ,name='liquidaciones'),
    path('mantenimiento-variables/', MantenimientoVariablesListView.as_view() ,name='mantenimiento-variables'),
    path('mantenimiento-EESS/', MantenimientoEESSListView.as_view() ,name='mantenimiento-EESS'),
    path('importacion-INFORHUS/', ImportacionBaseListView.as_view() ,name='inforhus')

]