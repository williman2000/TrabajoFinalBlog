from django.contrib import admin
from .models import Post,Categoria, Comentario


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'titulo', 'categoria',
                    'destacado', 'visible', 'imagen','creado', 'modificado')
    search_fields = ('titulo', 'user__username', 'user__email')
    list_filter = ('creado', 'modificado')
    list_editable = ('titulo', 'categoria','destacado', 'visible', 'imagen' )

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ('url',)
        form = super(PostAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        form.base_fields['perfil'].initial = request.user.perfil
        return form

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'imagen')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'comentario', 'visible')
