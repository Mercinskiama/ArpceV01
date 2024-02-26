from django.http import HttpResponse
import mimetypes

def file_function(class_name, attribut):
    
    chtr=getattr(class_name, attribut)
    with open(chtr.path,'rb') as doc:
        mime_type = mimetypes.guess_type(chtr.path)
        #print(mime_type[0])
        response = HttpResponse(doc, content_type=mime_type[0])
        response['Content-Disposition'] = 'inline;filename={}'.format(chtr.name)
        return response