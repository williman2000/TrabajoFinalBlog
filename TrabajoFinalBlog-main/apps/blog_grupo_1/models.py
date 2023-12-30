from django.db import models

from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

from apps.users.models import Perfil


class Categoria(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    imagen = models.ImageField(upload_to='media', default='static/categoria/post_default.jpg')
    
    class Meta:
        ordering = ('titulo',)

    def __str__(self):
        return self.titulo

class Post (models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT)
    titulo = models.CharField(max_length=255, unique=True)
    url = models.SlugField(max_length=255, unique=True)
    resumen = RichTextField()
    contenido = RichTextField()
    vistas = models.PositiveIntegerField(default=0)
    destacado = models.BooleanField(default=False)

    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    visible = models.BooleanField(default=True)
         
    imagen = models.ImageField(upload_to='media', default='static/post/post_default.jpg')

    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
    class Meta():
            ordering = ('creado',)
    

    def save(self, *args, **kwargs):
        self.url = slugify(self.titulo)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.titulo} - {self.user.username}'


class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    comentario = models.CharField(max_length=5000)
    visible = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)


class Contacto(models.Model):
    nombre = models.CharField(max_length=70)
    email = models.EmailField(max_length=50)
    asunto = models.CharField(max_length=100)
    mensaje = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)
