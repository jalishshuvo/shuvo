from django.contrib import admin

from .models import Author,Category,Post,Comment,PostView

# Register your models here.
admin.site.register(Author)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title','slug',)
    prepopulated_fields ={'slug':('title',)}
admin.site.register(Category,CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display=('title','author','published','status')
    prepopulated_fields ={'slug':('title',)}

admin.site.register(Post,PostAdmin)

admin.site.register(Comment)
admin.site.register(PostView)