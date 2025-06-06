from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify

def generate_unique_slug(instance, new_slug=None):
    slug = new_slug if new_slug else slugify(instance.title)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug)
    if qs.exists():
        new_slug = f"{slug}-{qs.count() + 1}"
        return generate_unique_slug(instance, new_slug=new_slug)
    return slug

class Post(models.Model):
    title           = models.CharField(max_length=255)
    description     = models.TextField(blank=True)
    author          = models.CharField(max_length=255, blank=True, null=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    published       = models.BooleanField(default=False)
    slug            = models.SlugField(max_length=255, unique=True, blank=True)
    cover_image     = models.ImageField(upload_to='post_covers/', blank=True, null=True)
    language        = models.CharField(max_length=30, blank=True, null=True)
    average_rating  = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_count    = models.PositiveIntegerField(default=0)
    currency        = models.CharField(max_length=10, default='USD')
    available       = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def short_description(self):
        return self.description[:100] + '...' if len(self.description) > 100 else self.description

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', kwargs={'slug': self.slug})


class PostSection(models.Model):
    post        = models.ForeignKey(Post, related_name='sections', on_delete=models.CASCADE)
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug        = models.SlugField(max_length=255, unique=True, blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.post.title})"


class SectionContentBlock(models.Model):
    section        = models.ForeignKey(PostSection, on_delete=models.CASCADE, related_name='content_blocks')
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes      = models.TextField(blank=True)

    class Meta:
        unique_together = ('section', 'content_type', 'object_id')

    def __str__(self):
        return f"ContentBlock #{self.pk} in Section '{self.section.title}'"


class Paragraph(models.Model):
    title      = models.CharField(max_length=255, blank=True)
    text       = models.TextField(max_length=128000)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else self.text[:30] + "..."

    def summary(self):
        return self.text[:100] + "..." if len(self.text) > 100 else self.text


class Image(models.Model):
    name       = models.CharField(max_length=255, blank=True)
    image      = models.ImageField(upload_to='section_images/')
    caption    = models.CharField(max_length=255, blank=True)
    alt_text   = models.CharField(max_length=255, blank=True, help_text="Alternative text for the image")
    order      = models.PositiveIntegerField(default=0)
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    width      = models.PositiveIntegerField(null=True, blank=True)
    height     = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.caption or "No caption"


from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter

class CodeSnippet(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    code = models.TextField(max_length=128000)
    LANGUAGE_CHOICES = [
        ('py', 'Python'),
        ('js', 'JavaScript'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('csharp', 'C#'),
        ('golang', 'Go'),
        # kerak bo‘lsa ko‘paytirish mumkin
    ]
    language = models.CharField(max_length=30, choices=LANGUAGE_CHOICES, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    highlighted_code = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.code and self.language:
            try:
                lexer = get_lexer_by_name(self.language)
                formatter = HtmlFormatter(style="colorful", linenos=True)
                self.highlighted_code = highlight(self.code, lexer, formatter)
            except Exception as e:
                self.highlighted_code = self.code  # fallback
        super().save(*args, **kwargs)

    def __str__(self):
        lang = self.get_language_display() if self.language else "No language"
        title_part = f"{self.title} - " if self.title else ""
        return f"{title_part}CodeSnippet ({lang}): {self.code[:30]}..."

class Video(models.Model):
    title = models.CharField(max_length=255, blank=True)
    video_file = models.FileField(upload_to='section_videos/')
    description = models.TextField(blank=True)
    duration = models.DurationField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or f"Video #{self.pk}"


class Document(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='section_documents/')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or f"Document #{self.pk}"


class Audio(models.Model):
    title = models.CharField(max_length=255, blank=True)
    audio_file = models.FileField(upload_to='section_audios/')
    description = models.TextField(blank=True)
    duration = models.DurationField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or f"Audio #{self.pk}"
