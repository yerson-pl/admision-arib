from django import forms
from .models import Postulante
from django.conf import settings


class PostulanteForm(forms.ModelForm):
    #fecha_nac = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    fecha_nac=forms.DateField(label='Fecha de Nacimiento',  widget=forms.TextInput(attrs={'placeholder': 'dd/mm/aaaa'}))
    class Meta:
        model = Postulante
        fields = ['dni_num', 'ap_paterno', 'ap_materno',
                  'nombre', 'sexo', 'fecha_nac', 'departamento',
                  'provincia', 'distrito', 'direccion', 'correo',
                  'inst_procedencia', 'egreso','celular', 'carrera',
                  'seg_carrera', 'foto', 'dni', 'certificado',
                  'num_operacion', 'voucher', 'dec_juarada'] 
    
    #dni_num = forms.IntegerField(label= 'DNI', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Introduzca su N° DNI'}))
    #ap_paterno = forms.IntegerField( required=True, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellido Paterno'}))

    
    
    #def __init__(self, *args, **kwargs):
    #class Meta:
    #    model = Postulante
        #fields = '__all__'
        #fields = ['dni_num', 'ap_paterno', 'ap_materno','foto', 'dec_juarada'] 
        #fields = ['dni_num', 'ap_paterno', 'ap_materno',
        #          'nombre', 'sexo', 'fecha_nac', 'departamento',
        #          'provincia', 'distrito', 'direccion', 'correo',
        #          'inst_procedencia', 'egreso','celular', 'carrera',
        #          'seg_carrera', 'foto', 'dni', 'certificado',
        #          'num_operacion', 'voucher', 'dec_juarada'] 
        