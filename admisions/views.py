from io import BytesIO
import locale


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from django.views import View
from django.urls import reverse
from django.core.mail import EmailMessage

from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils import timezone



from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Frame, TableStyle
# Create your views here.
#
#
from .forms import PostulanteForm
from .models import Postulante

styles = getSampleStyleSheet()
styleN = styles['Normal']
style = getSampleStyleSheet()
styleH = styles['Heading1']
#def Postulante(request):
#    if request.method == 'POST':
#        postulante_form = PostulanteForm(request.POST or None, request.FILES or None)
#        if postulante_form.is_valid():
#            postulante_form.save()
#            return redirect(reverse('admisions:inscripcion'), 'ok')
#            print(postulante_form)
#    else:
#        postulante_form = PostulanteForm()    
#        return redirect(reverse('admisions:inscripcion'), 'error')
#    return render(request, 'admision/admision_inscripcion.html', {'form':postulante_form})
#
#def crear(request):
#    if request.method == 'POST':
#        form = PostulanteForm(request.POST or None, request.FILES or None)
#        if form.is_valid():
#            form.save()
#            
#            return redirect(reverse('admisions:inscripcion'), 'ok')
#            print(form)
#        else:
#            form = PostulanteForm()
#        return redirect(reverse('admisions:inscripcion'), 'error')
#    return render(request, 'admision/admision_inscripcion.html', {'form_p': form})
#
#
def crearPostulante(request):
    if request.method == 'POST':
        #data = request.POST
        correo = request.POST.get('correo')
        ap_paterno = request.POST.get('ap_paterno')
        ap_materno = request.POST.get('ap_materno')
        nombre = request.POST.get('nombre')
        dni = request.POST.get('dni_num')
        carrera = request.POST.get('carrera')
        sexo = request.POST.get('sexo')
        seg_carrera = request.POST.get('seg_carrera')
        direccion = request.POST.get('direccion')
        distrito = request.POST.get('distrito')
        provincia = request.POST.get('provincia')
        celular = request.POST.get('celular')
        
        #created = request.POST.get('created')
        postulante_form = PostulanteForm(request.POST or None, request.FILES or None)
        if postulante_form.is_valid():
            template = get_template('admision/email.html')
            # Se renderiza el template y se envias parametros
            content = template.render({'email': correo, 'ap_paterno': ap_paterno, 'ap_materno': ap_materno,
                                        'nombre': nombre, 'dni':dni, 'sexo': sexo, 'carrera': carrera, 'seg_carrera': seg_carrera,
                                        'direccion': direccion, 'distrito':distrito, 'provincia':provincia, 'celular':celular,
                                        })
            email = EmailMultiAlternatives(
            'Inscripción admisión 2023 IESTP-ARIB',
            """
            Su inscripción al proceso de admisión al IESTP "ARIB" se ha realizado correctamente:
            """,
            settings.EMAIL_HOST_USER,
            [correo],  
        # ['bcc@example.com'],
        # reply_to=['another@example.com'],
        # headers={'Message-ID': 'foo'},
            )
            email.attach_alternative(content, 'text/html')
            email.send()
            postulante_form.save()
            return redirect(reverse('admisions:confirmacion'))
            postulante_form = PostulanteForm()
            print(postulante_form)
    else:
    	postulante_form = PostulanteForm()
        #return redirect(reverse('admisions:inscripcion'), 'error')
    return render(request, 'admision/admision_inscripcion.html', {'postulante_form':postulante_form})

class Email(TemplateView):
    template_name = 'admision/email.html'

class ConfirmacionView(TemplateView):
    template_name = 'admision/confirmacion.html'

class AdmisionHomeView(TemplateView):
    template_name = 'admision/admision_home.html'


class AdmisionInscripcionView(TemplateView):
    template_name = 'admision/admision_inscripcion.html'


class ReporteInscripcionPdf(View):
    def __init__(self):
        self.PAGE_SIZE = (8.27*inch, 11.69*inch)
        #self.c = canvas.Canvas(response, pagesize=self.PAGE_SIZE)
        self.styles = style
        self.width, self.height = self.PAGE_SIZE

    def cabecera(self,pdf):

        logo_minedu = "data:image/png;base64,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"
        #pdf.drawImage(logo_minedu, 450, 750, 120, 90, preserveAspectRatio=True)
        pdf.drawImage(logo_minedu, 20, 760, 120, 90, preserveAspectRatio=True)
        logo = "https://drive.google.com/uc?export=download&id=1Ku7Ecjc-zFkoRSHFfExAdf1oxVSj-yyO"
        pdf.drawImage(logo, 450, 775, 120, 45, preserveAspectRatio=True)
        #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 16)
        #Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(180, 800, u"ADMISIÓN 2023 I.E.S.T.P. - ARIB")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(220, 780, u"FICHA DE INSCRIPCIÓN")


    def tabla(self, pdf, y):
        encabezados = ('DNI', 'Nombre', 'Apellido Paterno', 'Apellido Materno')

        table = Table([encabezados], colWidths=2.25*inch)
        table.setStyle([#La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black), 
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 9)
                        ])
        table.wrapOn(pdf, 400, 500)
        table.drawOn(pdf, 10, y)


    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)
        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        y = 600
        self.tabla(pdf, y)
        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response                





class Listar(ListView):
    model = Postulante
    template_name = ('admision/list.html')


def listar(request):
    postulantes = Postulante.objects.all()
    print(postulantes)
    return render(request, 'admision/list.html', {'postulantes': postulantes})




def postulante_print(self, pk=None):  
    import io  
    from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle  
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle 
    from reportlab.lib import colors  
    from reportlab.lib.pagesizes import letter  
    from reportlab.platypus import Table, Image, SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
    from reportlab.lib.units import cm, inch, mm
    from reportlab.rl_settings import canvas_basefontname
    from reportlab.lib.fonts import tt2ps
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT, TA_LEFT
  
    
    response = HttpResponse(content_type='application/pdf')  
    buff = io.BytesIO()  
    doc = SimpleDocTemplate(
        buff,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=1 * cm,
        bottomMargin=1 * cm,
        title='Ficha de inscripción',
        author='IESTP - ARIB',
    ) 
    elements = []  
    styles = getSampleStyleSheet()
    titulo1 = ParagraphStyle(name='Titulo1',
                             parent=styles['Heading3'],
                             fontName=tt2ps(canvas_basefontname, 1, 0),
                             fontSize=12,
                             leading=14,
                             spaceBefore=10,
                             spaceAfter=1,
                             alignment=TA_CENTER
                             )
    titulo2 = ParagraphStyle(name='Titulo2',
                             parent=styles['Heading3'],
                             fontName=tt2ps(canvas_basefontname, 1, 0),
                             fontSize=12,
                             leading=14,
                             spaceBefore=0,
                             spaceAfter=20,
                             alignment=TA_CENTER
                             )

    secciones = styles['Heading4']
    cabecera = ParagraphStyle(name='Cabecera',
                              parent=styles['Normal'],
                              alignment=TA_CENTER,
                              fontSize=8,
                              leading=10
                              )

    paragraph = styles['Normal']
    paragraph.alignment = TA_JUSTIFY

    firma = ParagraphStyle(name='firma',
                           fontName=styles['Normal'],
                           alignment=TA_CENTER,
                           fontSize=10,
                           leading=10)

    lugar_fecha = styles['Italic']
    lugar_fecha.alignment = TA_RIGHT
    image1 = Image('data:image/png;base64,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', (291 / 8) * mm, (58 / 8) * mm)
    image2 = Image('https://drive.google.com/uc?export=download&id=1Ku7Ecjc-zFkoRSHFfExAdf1oxVSj-yyO', (669 / 20) * mm, (280 / 20) * mm)
    # elements.append(image1)
    logobj = [
        (
            image1,
            Paragraph("""INSTITUTO DE EDUCACIÓN SUPERIOR TECNOLÓGICO PÚBLICO<br/>
            "Alianza Renovada Ichuña Bélgica"<br/>
            Resolución Ministerial N° 0353-2004-ED<br/>
            Provincia General Sanchez Cerro - Distrito de Ichuña - Calle Tacna S/N
            """, cabecera),
            image2
        )
    ]
    logo_table = Table(logobj, [1.6 * inch, 3.7 * inch, 1.3 * inch])
    # logo_table.setStyle(PIE_TABLE)
    logo_table.setStyle(TableStyle([('ALIGN', (0, 0), (0, 0), 'LEFT'),
                                    ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),
                                    ('ALIGN', (0, 1), (0, 1), 'CENTER'),
                                    # ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                                    # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                    # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                    ]))
    elements.append(logo_table)

    elements.append(Paragraph("FICHA DE INSCRIPCIÓN", titulo1))
    elements.append(Paragraph("DEL POSTULANTE AL PROCESO DE ADMISIÓN DEL IESTP ARIB - 2023", titulo2))
    elements.append(Paragraph("I. DATOS PERSONALES:", secciones))
    elements.append(Spacer(10, 20))

    if not pk:  
      todaspostulantes = [(p.id, p.dni_num, p.ap_paterno, p.ap_materno, 
                          p.nombre, p.sexo)  
                for p in Postulante.objects.all().order_by('pk')]  
    else:  
      todaspostulantes = [(p.id, p.dni_num, p.ap_paterno, p.ap_materno, 
                          p.nombre, p.sexo)  
                for p in Postulante.objects.filter(id=pk)]
    headings = ('Id','DNI', 'Apellido Paterno', 'Apellido Materno', 'Nombres', 'Sexo')    
    t = Table([headings] + todaspostulantes)  
    t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                                ('VALIGN', (0, 0), (0, -1), 'TOP'),
                                ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.dodgerblue),
                                ('BOX', (0, 0), (-1, -1), 0.25, colors.darkblue),
                                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
                                ]))
    t.hAlign = TA_LEFT
    elements.append(t)

    elements.append(Paragraph("II. LUGAR DE NACIMIENTO:", secciones))
    elements.append(Spacer(10, 20))

    if not pk:  
      todaspostulantes = [(p.id, p.direccion, p.distrito, p.provincia, 
                          p.departamento)  
                for p in Postulante.objects.all().order_by('pk')]  
    else:  
      todaspostulantes = [(p.id, p.direccion, p.distrito, p.provincia, 
                          p.departamento)  
                for p in Postulante.objects.filter(id=pk)]
    headings = ('Id','Lugar', 'Distrito', 'Provincia', 'Departamento')    
    t = Table([headings] + todaspostulantes)  
    t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                                ('VALIGN', (0, 0), (0, -1), 'TOP'),
                                ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.dodgerblue),
                                ('BOX', (0, 0), (-1, -1), 0.25, colors.darkblue),
                                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
                                ]))
    t.hAlign = TA_LEFT
    elements.append(t)

    elements.append(Paragraph("III. INFORMACIÓN ACADÉMICA:", secciones))
    elements.append(Spacer(10, 20))

    if not pk:  
      todaspostulantes = [(p.id, p.inst_procedencia, p.egreso, p.celular)  
                for p in Postulante.objects.all().order_by('pk')]  
    else:  
      todaspostulantes = [(p.id, p.inst_procedencia, p.egreso, p.celular)  
                for p in Postulante.objects.filter(id=pk)]
    headings = ('Id','Colegio Procedencia', 'Año de Egreso', 'N° Celular', )    
    t = Table([headings] + todaspostulantes)  
    t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                                ('VALIGN', (0, 0), (0, -1), 'TOP'),
                                ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.dodgerblue),
                                ('BOX', (0, 0), (-1, -1), 0.25, colors.darkblue),
                                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
                                ]))
    t.hAlign = TA_LEFT
    elements.append(t)


    elements.append(Paragraph("IV. PROGRAMA DE ESTUDIOS AL CUAL POSTULAR:", secciones))
    elements.append(Spacer(10, 20))

    if not pk:  
      todaspostulantes = [(p.carrera, p.seg_carrera)  
                for p in Postulante.objects.all().order_by('pk')]  
    else:  
      todaspostulantes = [(p.carrera, p.seg_carrera)  
                for p in Postulante.objects.filter(id=pk)]
    headings = ('1ra Opcion Carrera', '2da Opcion Carrera')    
    t = Table([headings] + todaspostulantes)  
    t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                                ('VALIGN', (0, 0), (0, -1), 'TOP'),
                                ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                                ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.dodgerblue),
                                ('BOX', (0, 0), (-1, -1), 0.25, colors.darkblue),
                                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
                                ]))
    t.hAlign = TA_LEFT
    elements.append(t)

    elements.append(Spacer(20, 40))
    elements.append(Paragraph("""Declaro bajo juramento que los datos que consigno en la presente FICHA DE INSCRIPCIÓN, son verídicos y me remito para la confrontación con los documentos originales.
                De no ser correctos pierdo la vacante de admisión y renuncio a todo derecho que pueda
                obtener.""", paragraph))
    elements.append(Spacer(5, 10))
    today = timezone.now()
    #locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    elements.append(Paragraph(f"Ichuña, {today.strftime('%d de %B del %Y')}", lugar_fecha))

    elements.append(Spacer(20, 40))

    firma = [['__________________'],
             ['Firma']]
    firma_table = Table(firma)
    firma_table.setStyle(TableStyle([('VALIGN', (0, 0), (0, 0), 'BOTTOM'),
                                     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                     ('VALIGN', (1, 0), (1, 0), 'TOP'),
                                     # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                     # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                     ]))
    elements.append(firma_table)



    doc.build(elements)  
    response.write(buff.getvalue())  
    buff.close()  
    return response 