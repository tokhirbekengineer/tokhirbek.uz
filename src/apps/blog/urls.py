
from django.urls import path
from . import views
from .models import Paragraph, CodeSnippet
from .forms import ParagraphForm, CodeSnippetForm
urlpatterns = [
    # Post & Section
    path('', views.post_list, name='post_list'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/update/', views.post_update, name='post_update'),
    path('post/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('sections/create/', views.postsection_create, name='postsection_create'),
    path('sections/<int:pk>/', views.postsection_detail, name='postsection_detail'),
    path('sections/<int:pk>/edit/', views.postsection_update, name='postsection_update'),
    path('sections/<int:pk>/delete/', views.postsection_delete, name='postsection_delete'),
    # Generic ContentBlock delete         
    path('content/<str:model_name>/create/<int:section_id>/', views.generic_content_create, name='content_create'),
    path('content/<str:model_name>/update/<int:pk>/', views.generic_content_update, name='content_update'),
    path('content/<str:model_name>/delete/<int:pk>/', views.content_delete_view, name='content_delete'),
    # path('content/<str:model_name>/confirm_delete/<int:pk>/', views.generic_content_delete, name='contentblock_delete'),
    path('content/<str:model_name>/confirm_delete/<int:pk>/', views.generic_content_delete, name='contentblock_delete'),

]
