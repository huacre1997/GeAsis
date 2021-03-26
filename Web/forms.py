from django import forms
from .models import Usuario
from Web.models import *
from django.contrib.admin.widgets import FilteredSelectMultiple

from django.contrib.auth.models import Group
from django.conf import settings

from django import forms
from django.contrib.auth.forms import  PasswordResetForm, SetPasswordForm
class UserPasswordResetForm(SetPasswordForm):
    class Meta:
        model = Usuario
        fields="__all__"   
    def __init__(self,user,*args, **kwargs):

        self.user = user
     
       
       
        super(UserPasswordResetForm, self).__init__(user,*args, **kwargs)

    
    def clean(self):
        cleaned_data = super(UserPasswordResetForm,self).clean()

        n_pass = cleaned_data.get("new_pass")
        r_pass = cleaned_data.get("new_pass_repeat")
       
        if r_pass != n_pass:
            raise ValidationError("Las contraseñas no coinciden.")

   
        return self.cleaned_data
from django.contrib.auth import update_session_auth_hash
   
class UsuarioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(UsuarioForm, self).__init__(*args, **kwargs)
        print(self.request)
    class Meta:
        model = Usuario
        fields = ["groups","persona"]
        # widgets = {
        # 	'perfil': forms.SelectMultiple( attrs={'class':'selectpicker',}),
        # }
    
        widgets = {

                'groups': FilteredSelectMultiple("Permission", False,  attrs={'rows':'10'}),
         

            }
     
    def clean_groups(self):
        data=self.cleaned_data["groups"]
        if not data:
            raise forms.ValidationError("Debe asignar al menos un permiso.")

        return data    
    def clean_persona(self):
        data=self.cleaned_data["persona"]
        if data=="":
            raise forms.ValidationError("Este campo es obligatorio.")

        return data 
    def save(self, commit=True):
        data = {}
        form = super()
        print(form)
        try:
            if form.is_valid():
                passwd=self.instance.persona.nombres[0]+self.instance.persona.nro_doc
                u = form.save(commit=False)
                
                if u.pk is None:
                    print("if")
                    u.username=self.instance.persona.nro_doc

                    u.set_password(passwd)
                    if("Administrador" in [i.name for i in self.cleaned_data["groups"]]):
                        u.is_staff=True
                    print("set staff")
                else:
                    user = User.objects.get(pk=u.pk) 
                    if user.password != passwd:
                       u.set_password(passwd)

                print("antes del save")
                u.save(self.request.user.username,"Guardando usuario")
                print(u.persona.activo)
                print("despuesde ls ave")
                self.save_m2m()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
            print(e)
        return data
            
class  UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["username","groups"]
        # widgets = {
        # 	'perfil': forms.SelectMultiple( attrs={'class':'selectpicker',}),
        # }
      
        widgets = {
              
                'groups': FilteredSelectMultiple("Permission", False,  attrs={'rows':'10'}),

            }
    def clean_groups(self):
        data=self.cleaned_data["groups"]
        if not data:
            raise forms.ValidationError("Debe asignar al menos un permiso.")

        return data 