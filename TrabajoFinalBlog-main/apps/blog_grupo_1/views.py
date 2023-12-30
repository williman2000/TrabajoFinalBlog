import os
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post,Categoria, Comentario, Contacto
from .forms import CrearComentarioForm, PostForm, ContactoForm
from django.contrib.auth.models import Group

class PostCreateView(UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post/postear.html'
    success_url = reverse_lazy('blog:inicio')
    login_url = reverse_lazy('auth:login')

    def test_func(self):
        grupos = ['Administrador', 'Colaborador']
        return self.request.user.is_authenticated and any(self.request.user.groups.filter(name=grupo).exists() for grupo in grupos)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.perfil = self.request.user.perfil
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = 'Agregar Post'
        return context


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post/postear.html'
    slug_field = 'url'
    slug_url_kwarg = 'url'
    success_url = reverse_lazy('blog:inicio')
    login_url = reverse_lazy('auth:login')

    def test_func(self):
        grupos = ['Administrador']
        return self.request.user.is_authenticated and any(self.request.user.groups.filter(name=grupo).exists() for grupo in grupos) or self.request.user == self.get_object().user

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.perfil = self.request.user.perfil
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = 'Actualizar Post'
        return context


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    slug_field = 'url'
    slug_url_kwarg = 'url'
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:inicio')
    login_url = reverse_lazy('auth:login')

    def test_func(self):
        grupos = ['Administrador', 'Colaborador']
        return self.request.user.is_authenticated and any(self.request.user.groups.filter(name=grupo).exists() for grupo in grupos) or self.request.user == self.get_object().user

    def form_valid(self, form):
        # Obtener el objeto Auto
        post = self.get_object()

        # Eliminar la imagen asociada
        if post.imagen:
            # Obtener la ruta completa del archivo de imagen
            image_path = post.imagen.path

            # Verificar si el archivo existe y eliminarlo
            if os.path.exists(image_path):
                os.remove(image_path)

        return super().form_valid(form)


class OrdenarMasNuevoListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posteos'
    paginate_by = 2
    queryset = Post.objects.filter(visible=True).order_by('-creado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = Categoria.objects.all()
        context['posteos_destacados'] = Post.objects.filter(
            destacado=True, visible=True)
        return context
    
class OrdenarAZListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posteos'
    paginate_by = 2
    queryset = Post.objects.filter(visible=True).order_by('titulo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = Categoria.objects.all()
        context['posteos_destacados'] = Post.objects.filter(
            destacado=True, visible=True)
        return context
    
class OrdenarZAListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posteos'
    paginate_by = 2
    queryset = Post.objects.filter(visible=True).order_by('-titulo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = Categoria.objects.all()
        context['posteos_destacados'] = Post.objects.filter(
            destacado=True, visible=True)
        return context    
    
class OrdenarMasAntiguoListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posteos'
    paginate_by = 2
    queryset= Post.objects.filter(visible=True).order_by('creado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = Categoria.objects.all()
        context['posteos_destacados'] = Post.objects.filter(
            destacado=True, visible=True)
        return context
    
class InicioListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posteos'
    paginate_by = 2
    ordering = ('-creado',)
    queryset = Post.objects.filter(visible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = Categoria.objects.all()
        context['posteos_destacados'] = Post.objects.filter(
            destacado=True, visible=True)
        return context
    

class NosotrosTemplateView(TemplateView):
    template_name = 'blog/nosotros.html'

class PerfilTemplateView(TemplateView):
    template_name = 'blog/perfil.html'

class ContactoFormView(FormView):
    form_class = ContactoForm
    template_name = 'blog/contacto.html'
    success_url = reverse_lazy('blog:contactook')


class ContactoTemplateView(TemplateView):
    template_name = 'blog/contactook.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detalle.html'
    context_object_name = 'post'
    slug_field = 'url'
    slug_url_kwarg = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posteos'] = Post.objects.filter(visible=True)
        context['categoria'] = Categoria.objects.all()
        context['comentarios'] = Comentario.objects.filter(
            visible=True, post=self.get_object()).all()
        context['cantidad_comentarios'] = Comentario.objects.filter(
            visible=True, post=self.get_object()).all().count()
        return context


class ComentarioCreateView(UserPassesTestMixin, CreateView):
    model = Comentario
    form_class = CrearComentarioForm
    template_name = 'blog/detalle.html'
    login_url = reverse_lazy('auth:login')

    def test_func(self):
        grupos = ['Colaborador', 'Administrador', 'Registrado']
        return self.request.user.is_authenticated and any(self.request.user.groups.filter(name=grupo).exists() for grupo in grupos)

    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden("Acceso denegado. Método no permitido.")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.perfil = self.request.user.perfil
        return super().form_valid(form)

    def get_success_url(self):
        url = self.request.POST.get('url')
        return reverse_lazy('blog:detalle', kwargs={'url': url})

    def form_invalid(self, form):
        return HttpResponseServerError("Error interno al procesar el formulario.")


class ComentarioDeleteView(UserPassesTestMixin, DeleteView):
    model = Comentario
    template_name = 'blog/comentario_confirm_delete.html'
    login_url = reverse_lazy('auth:login')

    def test_func(self):
        grupos = ['Administrador', 'Colaborador']
        return self.request.user.is_authenticated and any(self.request.user.groups.filter(name=grupo).exists() for grupo in grupos) or self.request.user == self.get_object().user

    def get_success_url(self):
        url = self.object.post.url
        return reverse_lazy('blog:detalle', kwargs={'url': url})


class CategoriaListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posteos'
    paginate_by = 2
    ordering = ('titulo',)

    def get_queryset(self):
        post = None
        if self.kwargs['categoria_id']:
            categoria_id = self.kwargs['categoria_id']
            categoria = Categoria.objects.filter(id=categoria_id)[:1]
            post = Post.objects.filter(visible=True, categoria=categoria)
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria'] = Categoria.objects.all()
        context['posteos_destacados'] = Post.objects.filter(
            destacado=True, visible=True)
        return context


class UserListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posteos'
    paginate_by = 2
    ordering = ('-creado',)
    
    def get_queryset(self):
        auto = None
        if self.kwargs['nombre']:
            user_nombre = self.kwargs['nombre']
            user = User.objects.filter(username=user_nombre)[:1]
            post = Post.objects.filter(visible=True, user=user)
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['posteos_destacados'] = Post.objects.filter(
            destacado=True, visible=True)
        return context
