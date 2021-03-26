import csv,io,sys
from ..models import Establecimiento
from django.contrib import messages

def importExcel(request,file):
    # Establecimiento.objects.all().delete()
    # fhand=open("Web/scripts/test5.csv",encoding='utf-8')
    data_set = file.read().decode('utf-8-sig')
    io_string = io.StringIO(data_set)

    reader=csv.DictReader(io_string,delimiter=';', quotechar='"')
    try:
        for i,row in enumerate(reader):
            data=Establecimiento.objects.update_or_create(codigo=row["Código Único"],defaults={
            "institucion":row["Institución"],
            "codigo":row["Código Único"],
            "descripcion":row["Nombre del establecimiento"],
            "clasificacion":row["Clasificación"],
            "tipo":row["Tipo"],
            "departamento":row["Departamento"],
            "provincia":row["Provincia"],
            "distrito":row["Distrito"],
            "ubigeo":row["UBIGEO"],
            "direccion":row["Dirección"],
            "codigo_disa":row["Código DISA"],
            "codigo_red":row["Código Red"],
            "codigo_microred":row["Código Microrred"],
            "disa":row["DISA"],
            "red":row["Red"],
            "microred":row["Microrred"],
            "codigo_ue":row["Código UE"],
            "unidad_ejecutora":row["Unidad Ejecutora"],
            "categoria":row["Categoria"],
            "telefono":row["Teléfono"],
            "tip_categorizacion":row["Tipo Doc.Categorización"],
            "doc_categorizacion":row["Nro.Doc.Categorización"],
            "horario":row["Horario"],
            "inicio_actividad":row["Inicio de Actividad"],
            "responsable":row["Director Médico y/o Responsable de la Atención de Salud"],
            "estado":row["Estado"],
            "norte":row["NORTE"],
            "este":row["ESTE"],
            "cota":row["COTA"],
            "camas":row["CAMAS"],
            "ruc":row["RUC"],
                
                
                })
            print(data)
    except csv.Error as e:
        print(e)
        sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    return True