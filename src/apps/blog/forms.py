from django import forms
from .models import Post, PostSection

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'author', 'published', 'cover_image', 'language', 'currency', 'available']



class PostSectionForm(forms.ModelForm):
    class Meta:
        model = PostSection
        fields = ['post', 'title', 'description', 'is_active']


from django import forms
from .models import Paragraph, Image, Video, CodeSnippet, Document

class ParagraphForm(forms.ModelForm):
    class Meta:
        model = Paragraph
        fields = ['title', 'text', 'is_active']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['name', 'image', 'caption', 'alt_text', 'order', 'is_active']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file', 'description', 'duration', 'is_active']

class CodeSnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = ['title', 'code', 'language', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'code': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 10}),
            'language': forms.Select(attrs={'class': 'form-select'}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file', 'description', 'is_active']
