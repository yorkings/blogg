from django.contrib import admin
from blog.models import *
# Register your models here.
admin.site.register([Author,Content,Category])
class start(admin.ModelAdmin):
    list_display=['username','email','text']
admin.site.register(Comment,start)    