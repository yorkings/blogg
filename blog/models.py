from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.user.username


class Content(models.Model):
    tag = TaggableManager()

    class Status(models.TextChoices):
        PUBLISH = 'pb', 'Published'
        CREATED = 'CR', 'Created'

    title = models.CharField(max_length=200)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.OneToOneField(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    content = models.TextField()
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.PUBLISH)

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='comments')
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    upload = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null = True)
    picture = models.ImageField(upload_to='profile_pictures')
    bio = models.TextField(max_length=500)

    def __str__(self):
        return (self.user)
