from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce.models import HTMLField
from sorl.thumbnail import ImageField
from django.utils import timezone
#from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

User = get_user_model() 

class Author(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20,unique=True)
    slug = models.SlugField(max_length =20,unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural ='categories'
    def get_absolute_url(self):
        return reverse('list_of_post_by_category',kwargs={
            'slug': self.slug
        })
        
        # args=[self.slug])
            
    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    STATUS_CHOIICES =(
        ('draft','Draft'),
        ('published','Published')
    )
    title = models.CharField(max_length=250)
    overview =models.TextField(max_length=250)
    published = models.DateTimeField(default=timezone.now)
    timestamp = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=9,choices=STATUS_CHOIICES,default='draft')
    #content = HTMLField(blank=True,null=True)
    contents = RichTextUploadingField(blank=True,null=True)
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    slug = models.SlugField(max_length=250,unique=True)
    previous_post = models.ForeignKey(
        'self',related_name='previous',on_delete=models.SET_NULL,blank=True,null=True)
    next_post = models.ForeignKey(
        'self',related_name='next',on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={
            'slug': self.slug
        })
        
    def get_update_url(self):
        return reverse('post-update',kwargs={
            'slug': self.slug
        })
        
    def get_delete_url(self):
        return reverse('post-delete',kwargs={
            'slug': self.slug
        })
        

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')
    
    # @property
    # def view_count(self):
    #     return PostView.objects.filter(post=self).count()

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

class PostView(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



