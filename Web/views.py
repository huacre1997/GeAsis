from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.http.response import HttpResponseRedirect,JsonResponse
from django.views.generic import FormView, CreateView, ListView, UpdateView,ListView
from django.contrib import messages, auth
import json
from .models import Usuario
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .forms import *
from .mixins import ValidateMixin
from django.contrib.auth import update_session_auth_hash

class IndexView(LoginRequiredMixin,TemplateView):
    template_name="base.html"
    login_url = "Web:login"
    
class LoginView(FormView):
    template_name = "login.html"
    success_url=reverse_lazy("Web:home")
    form_class = AuthenticationForm
    login_url = "Web:login"
    def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, form ):
        form=self.get_form()
        if(form.is_valid()):
            username = self.request.POST['username']
            password = self.request.POST['password']
            user = auth.authenticate(username=username, password=password)
     
            if user is not None and user.is_active:

                auth.login(self.request, user)
                messages.success(self.request,f"Bienvenido {self.request.user}",extra_tags="login")

                data={"status":200}
            else:
                auth.logout(self.request)    
                data={"status":500,"error":"Este usuario está desactivado."}
                
        else:
            data={"status":500,"error":form.errors}
        return JsonResponse(data,safe=False)
    
class UserListView(LoginRequiredMixin,ValidateMixin,ListView):
    model=Usuario
    template_name="Seguridad/usuarios.html"
    login_url = "Web:login"
    permission_required=["Web.view_usuario"]

    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            print(action)
            if action=="searchData":
                data=[]
                for i in Usuario.objects.all().order_by("date_joined"):
                    data.append(i.toJSON())   
            else:
                data["error"]="Ha ocurrido un error aea"
        except Exception as e:
            print(e)
        return JsonResponse(data,safe=False)

class UsuarioCreateView(LoginRequiredMixin,ValidateMixin, CreateView):
    model=Usuario
    template_name = 'Seguridad/usuario.html'
    success_url = reverse_lazy("Web:usuarios")
    form_class=UsuarioForm
    permission_required=["Web.add_usuario"]
    login_url=reverse_lazy("Web:login")
    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(UsuarioCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    def post(self,request,*args, **kwargs):
        try:
            form = self.get_form()
            if form.is_valid():       
                form.save(request.user.username)    
                return JsonResponse({"status":200,"url":self.success_url})
            else:
                return JsonResponse({"status":500,"form":form.errors})  
        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["persona"] = Persona.objects.filter(activo=False) 
        return context
    
from .forms import UsuarioEditForm
class UsuarioUpdateView(LoginRequiredMixin,ValidateMixin, UpdateView):
    login_url=reverse_lazy("Web:login")
    model = Usuario
    template_name = 'Seguridad/usuarioedit.html'
    context_object_name="usuario"
    form_class=UsuarioEditForm
    success_url=reverse_lazy("Web:usuarios")
    permission_required=["Web.change_usuario"]
    def dispatch(self,request,*args, **kwargs):     
        self.object=self.get_object() 
        return super().dispatch(request,*args,**kwargs)

    def post(self,request,*args, **kwargs):
        try:
            form = self.get_form()
            if form.is_valid():
                print(self.object)      
                self.object.groups.clear()
                self.object.groups.set(form.cleaned_data["groups"])       
                if("Administrador" in [i.name for i in self.object.groups.all()]):
                    self.object.is_staff=True
                self.object.save(request.user.username)    
                return JsonResponse({"status":200,"url":self.success_url})
            else:
                data = {
                "form":form.errors,
                'status': 500,
                }
                return JsonResponse(data)      
        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)

class UsuarioUpdatePasswordView(LoginRequiredMixin,UpdateView):
    # login_url=reverse_lazy("Web:login")
    model = Usuario
    template_name = 'Seguridad/usuarioChangePassword.html'
    form_class = UserPasswordResetForm
    success_url = reverse_lazy("Web:usuarios")

    def dispatch(self,request,*args, **kwargs):     
        self.object=self.get_object() 
        return super().dispatch(request,*args,**kwargs)
    
    def get(self,*args, **kwargs):
        form = UserPasswordResetForm(user=self.object)
        return render(self.request,self.template_name,{"usuario":self.object,"form":form})
    def post(self,*args, **kwargs):
        try:
            form = UserPasswordResetForm(user=self.object,data=self.request.POST)
            if form.is_valid():
                
                data=form.save(commit=False)
                data.change=True
                data.save()
                update_session_auth_hash(self.request, data)

                return JsonResponse({"status":200})
            else:
                data = {
                    "form":form.errors,
                    'status': 500,
                    }
                return JsonResponse(data)
        except Exception as e:
            print(e)
            messages.error(self.request, 'Algo salió mal.Intentel nuevamente.')
            return HttpResponseRedirect(self.success_url)
def UsuarioDesactivate(request,pk):
    if request.method=="POST":
        user=Usuario.objects.filter(id=pk)
        if user.exists():
            data=user.first()
            data.is_active=False
            data.modified_by=request.user
            data.save(request.user.username,"Usuario desactivado")
            return JsonResponse({"status":200})
        else:
            return JsonResponse({"status":404})
def UsuarioActivate(request,pk):
    if request.method=="POST":
        user=Usuario.objects.filter(id=pk)
        if user.exists():
            data=user.first()
            data.is_active=True
            data.modified_by=request.user

            data.save(request.user.username,"Usuario activado")
            return JsonResponse({"status":200})
        else:
            return JsonResponse({"status":404})
def UsuarioResetPasswordView(request,pk):
    if request.method=="POST":
        user=Usuario.objects.filter(id=pk)
        if user.exists():
            data=user.first()
            passwd=data.persona.nombres[0]+data.persona.nro_doc            
            data.set_password(passwd)
            data.last_login=None
            data.save()
            return JsonResponse({"status":200})
        else:
            return JsonResponse({"status":404})
from .scripts.many_load import importExcel
def run(request):
    if request.method=="POST":
        file=request.FILES['SSEE']
        if not file.name.endswith('.csv'):
            messages.error(request, 'El archivo cargado no es .csv')
        else:
            if importExcel(request,file):
                print("if")
                messages.success(request, 'Archivo cargando...')
            print("fuera del uf")
        return HttpResponseRedirect(reverse_lazy("Web:home"))
class EstablecimientoListView(LoginRequiredMixin,ValidateMixin,ListView):
    model=Usuario
    template_name="establecimientos.html"
    login_url = "Web:login"
    permission_required=["Web.view_usuario"]

    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            print(action)
            if action=="searchData":
                data=[]
                for i in Establecimiento.objects.all():
                    data.append(i.toJSON())   
            else:
                data["error"]="Ha ocurrido un error aea"
        except Exception as e:
            print(e)
        return JsonResponse(data,safe=False)
class ProgramacionListView(LoginRequiredMixin,TemplateView):
    template_name="programacion.html"
class LiquidacionListView(LoginRequiredMixin,TemplateView):
    template_name="liquidacion.html"
class MantenimientoVariablesListView(LoginRequiredMixin,TemplateView):
    template_name="mantenimientoVariables.html"
class MantenimientoEESSListView(LoginRequiredMixin,TemplateView):
    template_name="mantenimientoEESS.html"
class ImportacionBaseListView(LoginRequiredMixin,TemplateView):
    template_name="importacionBase.html"