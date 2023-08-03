from django.contrib import admin
from blog.models import *
# Register your models here.
admin.site.register([Category])
class start(admin.ModelAdmin):
    list_display=['username','email','text']
admin.site.register(Comment,start)    

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display=['title','slug','category','author','created_at','published']
    prepopulated_fields = {'slug': ('title',)}