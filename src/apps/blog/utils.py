from .models import Paragraph, CodeSnippet, Image, Video, Document
from .forms import ParagraphForm, CodeSnippetForm, ImageForm, VideoForm, DocumentForm


# Model nomi bo‘yicha Model klassini olish
def get_model_by_name(model_name):
    mapping = {
        'paragraph': Paragraph,
        'codesnippet': CodeSnippet,
        'image': Image,
        'video': Video,
        'document': Document,
    }
    return mapping.get(model_name)


# Model nomi bo‘yicha Form klassini olish
def get_form_by_model_name(model_name):
    mapping = {
        'paragraph': ParagraphForm,
        'codesnippet': CodeSnippetForm,
        'image': ImageForm,
        'video': VideoForm,
        'document': DocumentForm,
    }
    return mapping.get(model_name)


# Uchlik: Model, Form va Template birga
CONTENT_MODELS = {
    'paragraph': (Paragraph, ParagraphForm, 'admin/content_form.html'),
    'codesnippet': (CodeSnippet, CodeSnippetForm, 'admin/code/codesnippet_form.html'),
    'image': (Image, ImageForm, 'admin/image/image_form.html'),
    'video': (Video, VideoForm, 'admin/video/video_form.html'),
    'document': (Document, DocumentForm, 'document/document_form.html'),
}


from django.http import HttpResponseForbidden
from functools import wraps

def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Sizda bu amalni bajarishga ruxsat yo'q.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

