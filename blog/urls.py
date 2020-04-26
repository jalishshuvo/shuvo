"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from posts.views import (index,blog,post_detail,search,post_create,post_update,
                        post_delete,list_of_post_by_category,about,privacy)
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),
    path('about/',about),
    path('privacy/',privacy),
    
    path('blog/',blog, name = 'post-list'),

    path('search/',search,name='search'),

    path('create/',post_create, name = 'post-create'),
    path('<slug>/',post_detail, name = 'post-detail'),
    path('<slug>/update/', post_update,name='post-update' ),
    
    path('<slug>/delete/',post_delete, name = 'post-delete'),

    path('category/<category_slug>/',list_of_post_by_category,name = 'list_of_post_by_category'),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/',include('ckeditor_uploader.urls'))

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)