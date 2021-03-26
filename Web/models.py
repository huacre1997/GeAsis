from django.db import models
from ModelTracker import Tracker
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission, BaseUserManager
from django.forms import model_to_dict
from Web.constants import *
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

class EstableciminetoAIRHSP(models.Model):
    codigo=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=100)
class NivelPLH(models.Model):
    codigo=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=100)
class NivelRemunerativo(models.Model):
    codigo=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=100)
class Cargo(models.Model):
    codigo=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=100)
class Universidad(models.Model):
    codigo=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=100)
class Especialidad(models.Model):
    codigo=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=100)
class Profesion(models.Model):
    codigo=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=100)
class Establecimiento(models.Model):
    institucion=models.CharField(max_length=50,null=True,blank=True)
    codigo=models.CharField(max_length=10,null=True,blank=True)
    descripcion=models.CharField(max_length=100,null=True,blank=True)
    clasificacion=models.CharField(max_length=100,null=True,blank=True)
    tipo=models.CharField(max_length=100,null=True,blank=True)
    departamento=models.CharField(max_length=50,null=True,blank=True)
    provincia=models.CharField(max_length=50,null=True,blank=True)
    distrito=models.CharField(max_length=50,null=True,blank=True)
    ubigeo=models.CharField(max_length=10,null=True,blank=True)
    direccion=models.CharField(max_length=200,null=True,blank=True)
    codigo_disa=models.CharField(max_length=5,null=True,blank=True)
    codigo_red=models.CharField(max_length=5,null=True,blank=True)
    codigo_microred=models.CharField(max_length=5,null=True,blank=True)
    disa=models.CharField(max_length=5,null=True,blank=True)
    red=models.CharField(max_length=50,null=True,blank=True)
    microred=models.CharField(max_length=20,null=True,blank=True)
    codigo_ue=models.CharField(max_length=10,null=True,blank=True)
    unidad_ejecutora=models.CharField(max_length=50,null=True,blank=True)
    categoria=models.CharField( max_length=50,null=True,blank=True)
    telefono=models.CharField( max_length=50,null=True,blank=True)
    tip_categorizacion=models.CharField( max_length=50,null=True,blank=True)
    doc_categorizacion=models.CharField( max_length=100,null=True,blank=True)
    horario=models.CharField(max_length=50,null=True,blank=True)
    inicio_actividad=models.CharField(max_length=20,null=True,blank=True)
    responsable=models.CharField(max_length=80,null=True,blank=True)
    estado=models.CharField(max_length=10,null=True,blank=True)
    norte=models.CharField( max_length=50,null=True,blank=True)
    este=models.CharField( max_length=50,null=True,blank=True)
    cota=models.CharField( max_length=50,null=True,blank=True)
    camas=models.CharField( max_length=10,null=True,blank=True)
    ruc=models.CharField( max_length=12,null=True,blank=True)
    def toJSON(self): 
      item = model_to_dict(self,fields=["codigo","descripcion","departamento","provincia","distrito","responsable"])
      return item
class Persona(Tracker.ModelTracker):
    id_rrhh=models.CharField(max_length=10,null=True,blank=True)
    valid_reniec=models.CharField(max_length=1,null=True,blank=True)
    tip_doc = models.CharField(
       choices=CHOICES_TIPO_DOC2,max_length=2,null=True,blank=True)
    nro_doc = models.CharField(max_length=15,null=True,blank=True)
    nombres=models.CharField(max_length=50,null=True,blank=True)
    ape_pat=models.CharField(max_length=50,null=True,blank=True)
    ape_mat=models.CharField(max_length=50,null=True,blank=True)
    ape_cada=models.CharField(max_length=50,null=True,blank=True)
    fech_nac = models.CharField(max_length=15, blank=True, null=True)
    sexo = models.CharField(max_length=1,choices=CHOICES_SEXO, blank=True, null=True)
    est_civil=models.CharField(max_length=1,null=True,blank=True)
    direc=models.CharField(max_length=150,null=True,blank=True)
    ruc=models.CharField(max_length=12,null=True,blank=True)
    correo=models.CharField(max_length=100,null=True,blank=True)
    telefono = models.CharField(max_length=100, null=True, blank=True)
    nivel_e=models.CharField(max_length=2,blank=True,null=True)
    grado_e=models.CharField(max_length=2,blank=True,null=True)
    profesion=models.ForeignKey(Profesion,on_delete=models.PROTECT,null=True,blank=True)
    condi_pro=models.CharField(max_length=2,blank=True,null=True)
    cole_pro=models.CharField(max_length=20,blank=True,null=True)
    t_espe=models.CharField(max_length=2,blank=True,null=True)
    especialidad=models.ForeignKey(Especialidad,on_delete=models.PROTECT,null=True,blank=True)
  
    establecimiento=models.ForeignKey(Establecimiento,  on_delete=models.PROTECT,null=True,blank=True)
    condi_esp=models.CharField(max_length=2,null=True,blank=True)
    rne=models.CharField( max_length=50,null=True,blank=True)
    universidad=models.ForeignKey(Universidad, on_delete=models.PROTECT,blank=True,null=True)
    ejerce=models.CharField(max_length=2,null=True,blank=True)
    maestria=models.CharField(max_length=2,null=True,blank=True)
    doctorado=models.CharField(max_length=2,null=True,blank=True)
    fec_1er_con=models.CharField(max_length=20,blank=True,null=True)
    fec_ingreso=models.CharField(max_length=20,null=True,blank=True)
    cargo=models.ForeignKey(Cargo,on_delete=models.PROTECT,null=True,blank=True)
    regimen=models.CharField(max_length=2,null=True,blank=True)
    condi_la=models.CharField(max_length=2,null=True,blank=True)
    nivel_re=models.ForeignKey(NivelRemunerativo, on_delete=models.PROTECT,null=True,blank=True)
    nivel_r_plh=models.ForeignKey(NivelPLH,on_delete=models.PROTECT, null=True,blank=True)
    fuente_f=models.CharField(max_length=3,null=True,blank=True)
    compensacion=models.CharField(max_length=20,null=True,blank=True)
    tipo_trabajo=models.CharField(max_length=50,null=True,blank=True)
    tareas_covid=models.CharField(max_length=2,null=True,blank=True)
    contratado_11=models.CharField(max_length=2,null=True,blank=True)
    motivo_covid=models.CharField(max_length=255,null=True,blank=True)
    prueba_tami=models.CharField(max_length=2,null=True,blank=True)
    kits_pro=models.CharField(max_length=2,null=True,blank=True)
    cant_kits=models.CharField(max_length=5,null=True,blank=True)
    descando_m=models.CharField(max_length=2,null=True,blank=True)
    fech_nom=models.CharField(max_length=20,null=True,blank=True)
    adj_pdf=models.CharField(max_length=2,null=True,blank=True)
    tip_per=models.CharField(max_length=2,null=True,blank=True)
    reg_infor=models.CharField(max_length=2,null=True,blank=True)
    condi_infor=models.CharField(max_length=2,null=True,blank=True)
    grupo_infor=models.CharField(max_length=2,null=True,blank=True)
    grupo_niv=models.CharField(max_length=2,null=True,blank=True)
    grupo_rep=models.CharField(max_length=2,null=True,blank=True)
    codpl_air=models.CharField(max_length=20,null=True,blank=True)
    codue_air=models.CharField(max_length=5,null=True,blank=True)
    tipop_air=models.CharField(max_length=5,null=True,blank=True)
    condreg_air=models.CharField(max_length=5,null=True,blank=True)
    codcon_air=models.CharField(max_length=5,null=True,blank=True)
    codgrup_air=models.CharField(max_length=5,null=True,blank=True)
    codcar_air=models.CharField(max_length=5,null=True,blank=True)
    estado_air=models.CharField(max_length=5,null=True,blank=True)
    codingre_air=models.CharField(max_length=5,null=True,blank=True)
    fec_ingresoi=models.CharField(max_length=20,null=True,blank=True)
    docing_air=models.CharField(max_length=10,null=False,blank=True)
    fecdoc_ing=models.CharField(max_length=20,null=True,blank=True)
    nrodoc_ing=models.CharField(max_length=50,blank=True,null=True)
    esta_air=models.ForeignKey(EstableciminetoAIRHSP, on_delete=models.PROTECT,blank=True,null=True)
    meta_air=models.CharField(max_length=20,null=True,blank=True)
    idgasto_air=models.CharField(max_length=5,null=True,blank=True)
    idfuen_air=models.CharField(max_length=5,null=True,blank=True)
    nro_meses=models.CharField(max_length=5,null=True,blank=True)
    banco=models.CharField(max_length=5,null=True,blank=True)
    tip_cuenta=models.CharField(max_length=5,null=True,blank=True)
    nro_cuenta=models.CharField(max_length=50,null=True,blank=True)
    cci=models.CharField(max_length=50,null=True,blank=True)
    idre_pen=models.CharField(max_length=5,null=True,blank=True)
    idre_pendes=models.CharField(max_length=5,null=True,blank=True)
    fech_renpen=models.CharField(max_length=20,null=True,blank=True)
    cuspp=models.CharField(max_length=20,null=True,blank=True)
    nro_carnees=models.CharField(max_length=50,null=True,blank=True)
    idusu_act=models.CharField(max_length=5,null=True,blank=True)
    est_registuspp=models.CharField(max_length=15,null=True,blank=True)
    fecini_cas=models.CharField(max_length=50,null=True,blank=True)
    fecfin_cas=models.CharField(max_length=50,null=True,blank=True)
    cargo_con=models.CharField(max_length=100,null=True,blank=True)
    id_pais=models.CharField(max_length=2,null=True,blank=True)
    pais=models.CharField(max_length=20,null=True,blank=True)
    renas_fin=models.CharField(max_length=20,null=True,blank=True)
    terceros=models.CharField(max_length=20,null=True,blank=True)
    activo=models.BooleanField(default=False)

    def __str__(self):
        return self.nombres+" "+self.ape_pat+" "+self.ape_mat
#    def get_image(self):
#         if self.foto_nueva:
#             return '{}{}'.format(settings.MEDIA_URL, self.foto_nueva)
#         return '{}{}'.format(settings.STATIC_URL, "img/img_avatar1.png")

#    def __str__(self):
#       return self.apep + ' ' + self.apem + ' ' + self.nom

    def toJSON(self):
      item = model_to_dict(self)
      item["establecimiento"] = self.establecimiento.descripcion
      return item
class Usuario(AbstractUser,Tracker.ModelTracker):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE,null=True,blank=True)
    change=models.BooleanField(default=False)


    def save(self, *args, **kwargs):
      # if self.persona:
      #   self.email=self.persona.correo
      if self.is_superuser:
        self.change=True
      super(Usuario, self).save(*args, **kwargs)
    

    def toJSON(self):
      item = model_to_dict(self)
      item["date_joined"]=self.date_joined.strftime('%Y-%m-%d')
      item["groups"]= item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
      item["persona"]=self.persona.nombres+" "+self.persona.ape_pat+""+self.persona.ape_mat
      return item
    def toJSON2(self):
      item = model_to_dict(self,exclude=["groups","date_joined"])
      item["persona"]=self.persona.nombres+" "+self.persona.apellidos
      return item
@receiver(post_save, sender=Usuario)
def save_user(sender, instance, **kwargs):
    if instance.persona: 
      instance.persona.activo=True
      instance.persona.save()