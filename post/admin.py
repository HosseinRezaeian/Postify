from django.contrib import admin
from .models import Picture, BlogPost,Like

# Register your models here.

admin.site.register(Picture)
admin.site.register(Like)


class PicturesLine(admin.TabularInline):
    model = Picture
    extra = 3


@admin.register(BlogPost)
class AdminProductClass(admin.ModelAdmin):
    list_display = ('title', 'slug', 'discription', 'create_by', 'datetime')
    inlines = [PicturesLine]
    prepopulated_fields = {'slug': ('title',)}
