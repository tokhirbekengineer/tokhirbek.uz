from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm  # keyin yaratamiz
from django.contrib.auth.decorators import user_passes_test

from django.core.paginator import Paginator
from django.db.models import Q

# POST LIST - Read
def post_list(request):
    query = request.GET.get('q', '')
    post_list = Post.objects.filter(published=True)

    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    post_list = post_list.order_by('-created_at')
    paginator = Paginator(post_list, 1)  # Har bir sahifada 5 post

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'user/post_list.html', {'posts': posts})
# POST DETAIL - Read
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    sections = post.sections.filter(is_active=True).order_by('created_at')
    return render(request, 'user/post_detail.html', {'post': post, 'sections': sections})

def post_create(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('access_denied')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'admin/post_form.html', {'form': form})

# POST UPDATE - Update
def post_update(request, slug):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('access_denied')

    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)
    return render(request, 'admin/post_form.html', {'form': form, 'post': post})

# POST DELETE - Delete
def post_delete(request, slug):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('access_denied')

    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'admin/post_confirm_delete.html', {'post': post})



from django.shortcuts import get_object_or_404
from .models import Post, PostSection
from .forms import PostSectionForm

def postsection_create(request):
    post_id = request.GET.get('post_id')
    post = get_object_or_404(Post, id=post_id) if post_id else None

    form = PostSectionForm(request.POST or None, initial={'post': post})
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('post_detail', slug=post.slug)

    return render(request, 'admin/section/post_section_form.html', {
        'form': form,
        'title': 'Create Section',
        'post': post,
    })

from .forms import PostSectionForm  # mavjud bo‘lishi kerak

def postsection_detail(request, pk):
    section = get_object_or_404(PostSection, pk=pk)
    post = section.post
    content_blocks = section.content_blocks.select_related('content_type').all()

    return render(request, 'user/section/post_section_detail.html', {
        'section': section,
        'post': post,
        'content_blocks': content_blocks,
    })



def postsection_update(request, pk):
    section = get_object_or_404(PostSection, pk=pk)
    form = PostSectionForm(request.POST or None, instance=section)
    if form.is_valid():
        form.save()
        return redirect('post_detail', slug=section.post.slug)
    return render(request, 'admin/section/post_section_form.html', {'form': form, 'title': 'Edit Section'})

def postsection_delete(request, pk):
    section = get_object_or_404(PostSection, pk=pk)
    if request.method == 'POST':
        post_slug = section.post.slug
        section.delete()
        return redirect('post_detail', slug=post_slug)
    return render(request, 'admin/section/post_section_confirm_delete.html', {'section': section})


from .models import Paragraph, CodeSnippet, Image, Video, Document
from .forms import ParagraphForm, CodeSnippetForm, ImageForm, VideoForm, DocumentForm

CONTENT_MODELS = {
    'paragraph': (Paragraph, ParagraphForm, 'admin/content_form.html'),
    'codesnippet': (CodeSnippet, CodeSnippetForm, 'admin/code/codesnippet_form.html'),
    'image': (Image, ImageForm, 'admin/image/image_form.html'),
    'video': (Video, VideoForm, 'admin/video/video_form.html'),
    'document': (Document, DocumentForm, 'document/document_form.html'),
}
from .utils import get_model_by_name, get_form_by_model_name, CONTENT_MODELS

# blog/views.py
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import SectionContentBlock, PostSection
from django.http import Http404

def generic_content_create(request, model_name, section_id):
    model_class, form_class, template = CONTENT_MODELS.get(model_name)
    return content_create_view(request, section_id, model_class, form_class, template)

def generic_content_update(request, model_name, pk):
    Model = get_model_by_name(model_name)
    content = get_object_or_404(Model, pk=pk)

    # content obyektiga tegishli SectionContentBlock ni olish
    section_block = SectionContentBlock.objects.filter(
        content_type=ContentType.objects.get_for_model(Model),
        object_id=content.pk
    ).first()

    if not section_block:
        raise ValueError("Content obyekti uchun tegishli SectionContentBlock topilmadi")

    section = section_block.section

    if request.method == 'POST':
        form = get_form_by_model_name(model_name)(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            return redirect('postsection_detail', pk=section.pk)
    else:
        form = get_form_by_model_name(model_name)(instance=content)

    context = {
        'form': form,
        'section': section,
        'create': False,
    }
    return render(request, 'admin/content_form.html', context)

# Generic CREATE
def content_create_view(request, section_id, model_class, form_class, template_name):
    section = get_object_or_404(PostSection, pk=section_id)
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            content_obj = form.save()
            SectionContentBlock.objects.create(
                section=section,
                content_type=ContentType.objects.get_for_model(model_class),
                object_id=content_obj.id
            )
            messages.success(request, f"{model_class.__name__} created successfully.")
            return redirect('postsection_detail', pk=section.id)
    else:
        form = form_class()
    return render(request, template_name, {'form': form, 'create': True, 'section': section})


# Generic UPDATE
def content_update_view(request, pk, model_class, form_class, template_name):
    obj = get_object_or_404(model_class, pk=pk)
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"{model_class.__name__} updated successfully.")
            section = obj.sectioncontentblock_set.first().section
            return redirect('postsection_detail', pk=section.id)
    else:
        form = form_class(instance=obj)
    return render(request, template_name, {'form': form, 'create': False})


# Generic DELETE
from django.contrib.contenttypes.models import ContentType

def content_delete_view(request, pk, model_class, template_name):
    obj = get_object_or_404(model_class, pk=pk)
    content_type = ContentType.objects.get_for_model(obj)
    # content_type va obj.id bo'yicha SectionContentBlock ni topamiz
    scb = SectionContentBlock.objects.filter(content_type=content_type, object_id=obj.pk).first()

    if not scb:
        # Agar bog‘liq bo‘lgan content block topilmasa, error yoki redirect qilishingiz mumkin
        messages.error(request, "Related content block not found.")
        return redirect('post_list')  # yoki kerakli sahifaga

    section = scb.section

    if request.method == 'POST':
        obj.delete()
        messages.success(request, f"{model_class.__name__} deleted successfully.")
        return redirect('postsection_detail', pk=section.pk)

    return render(request, template_name, {'object': obj})

from django.shortcuts import get_object_or_404, redirect
from apps.blog.models import Paragraph, CodeSnippet, Image, Video  # misol uchun

from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.contrib import messages

# def generic_content_delete(request, model_name, pk):
#     model_map = {
#         'paragraph': Paragraph,
#         'codesnippet': CodeSnippet,
#         'image': Image,
#         'video': Video,
#     }
#     content_block = get_object_or_404(SectionContentBlock, pk=pk, content_type__model=model_name)

#     model = model_map.get(model_name)
#     if not model:
#         raise Http404("Invalid model name")

#     obj = get_object_or_404(model, pk=pk)
    
#     # SectionContentBlock ni topamiz
#     content_type = ContentType.objects.get_for_model(model)
#     block = SectionContentBlock.objects.filter(content_type=content_type, object_id=obj.pk).first()

#     if not block:
#         messages.error(request, "Related content block not found.")
#         return redirect('post_list')  # yoki kerakli sahifa

#     section = block.section  # Bu orqali postsection ni aniqlaymiz

#     if request.method == 'POST':
#         obj.delete()  # content o‘chadi
#         block.delete()  # block ham o‘chadi
#         messages.success(request, f"{model.__name__} deleted successfully.")
#         return redirect('postsection_detail', pk=section.pk)

#     return render(request, 'blog/content_confirm_delete.html', {'object': obj})

# # from django.shortcuts import get_object_or_404, redirect
# # from django.contrib import messages
# # from apps.blog.models import SectionContentBlock

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from apps.blog.models import SectionContentBlock, Paragraph, CodeSnippet, Image, Video

def generic_content_delete(request, model_name, pk):
    # 1. Avvalo SectionContentBlock ni pk bo'yicha topamiz
    content_block = get_object_or_404(SectionContentBlock, pk=pk)
    
    # 2. Bog'liq model klassini model_name asosida aniqlaymiz
    model_map = {
        'paragraph': Paragraph,
        'codesnippet': CodeSnippet,
        'image': Image,
        'video': Video,
    }
    model = model_map.get(model_name)
    if not model:
        messages.error(request, "Invalid model name")
        return redirect('post_list')

    # 3. SectionContentBlock ichidagi content_object ni topamiz, bu esa model instance bo'lishi kerak
    obj = content_block.content_object
    if not obj or not isinstance(obj, model):
        messages.error(request, "Content object not found or type mismatch.")
        return redirect('post_list')

    section = content_block.section

    if request.method == 'POST':
        # 4. Ikkalasini ham o'chiramiz: content va content_block
        obj.delete()
        content_block.delete()
        messages.success(request, f"{model.__name__} deleted successfully.")
        return redirect('postsection_detail', pk=section.pk)

    # Agar confirm page kerak emas deyapsan, shu yerga render qilish kodini olib tashlash mumkin
    return redirect('postsection_detail', pk=section.pk)



def contentblock_delete(request, model_name, pk):
    block = get_object_or_404(SectionContentBlock, pk=pk)
    section = block.section
    if request.method == 'POST':
        block.delete()
        messages.success(request, "Content block deleted successfully.")
        return redirect('postsection_detail', pk=section.pk)
    # Agar GET so‘rov kelsa, oddiy redirect qilamiz yoki 405 qaytaramiz
    return redirect('postsection_detail', pk=section.pk)

