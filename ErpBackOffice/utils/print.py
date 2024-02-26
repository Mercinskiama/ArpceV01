from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from ErpBackOffice.dao.dao_print import *
import os
from django.conf import settings
from django.template import Context

from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from weasyprint.fonts import FontConfiguration
import tempfile
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


## import de tous les modules (Important pour la conversion html to pdf)
import ModuleApplication
import ModuleConfiguration
import ModuleConversation

# from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}, request = None):
    template = get_template(template_src)
    html  = template.render(context_dict)
    # result = BytesIO()
    # #links    = lambda uri, rel: os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    # #path = get_full_path_x(request)
    # pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    # if not pdf.err:
    #     return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def my_exec(code, id = None):
    exec('global i; i = %s' % code)
    global i
    return i

def the_import_exec(code, request):
    #print("code", code)
    exec('global i; i = ' + code)
    global i
    return i




def fetch_resources(uri, rel):
    media_rt = settings.BASE_DIR + "/templates/ErpProject/shared"
    media_url = 'file:///' + media_rt
    path = os.path.join(media_rt, uri.replace(media_url, ""))

    return path

def get_full_path_x(request):
    full_path = ('http', ('', 's')[request.is_secure()], '://',
    request.META['HTTP_HOST'], request.path)
    return ''.join(full_path)



def weasy_print_old(link, name, context):
    html_string = render_to_string(link, context)
    download_dir = settings.DOWNLOAD_DIR
    css_dir = settings.CSS_DIR

    font_config = FontConfiguration()
    html = HTML(string=html_string)
    css_print = CSS(os.path.join(css_dir,'print.css'), font_config=font_config)
    pdf_file = html.write_pdf(target=os.path.join(download_dir, name), stylesheets=[css_print], font_config=font_config)

    fs = FileSystemStorage(download_dir)
    with fs.open(name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(context['title'])
        return response
    
def weasy_print(link, name, context, request=None):
    html_string = render_to_string(link, context)
    css_dir = settings.CSS_DIR

    font_config = FontConfiguration()
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    css_print = CSS(os.path.join(css_dir,'print.css'), font_config=font_config)
    pdf_file = html.write_pdf(stylesheets=[css_print], presentational_hints=True)


    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(context['title'])
    return response






