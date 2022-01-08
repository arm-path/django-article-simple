from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Category, Section, Subject, Article


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    """Представление в административной панели, модели разделов"""
    list_display = ['title', 'slug']
    list_display_links = ['title']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Представление в административной панели, модели категорий"""
    list_display = ['title', 'slug']
    list_display_links = ['title']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Представление в административной панели, модели тем"""
    list_display = ['title', 'slug']
    list_display_links = ['title']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}


class ArticleContentForm(forms.ModelForm):
    """Добавление CKEditor формы, вместо формы поля content модели Article"""
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Представление в административной панели, модели статей"""
    form = ArticleContentForm
    list_display = ['title', 'section', 'category',
                    'subject', 'get_image', 'posted_by']
    list_display_links = ['title']
    search_fields = ['title']
    list_filter = ['section', 'category', 'subject', 'posted_by']
    list_editable = ['posted_by']
    fields = ['title', 'slug', 'section', 'category', 'subject', 'content_description', 'content',
              'image_publication', 'get_image', 'publication_date', 'update_date', 'posted_by']
    readonly_fields = ['get_image', 'publication_date', 'update_date']
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True
    actions = ['published', 'not_published']

    def get_image(self, obj):
        """Получение изображения, для отображения в административной панели"""
        if obj.image_publication:
            return mark_safe(f'<img src = "{obj.image_publication.url}" width = "150">')
        else:
            return "Изображение отсутствует"

    get_image.short_description = "Изображение"

    def published(self, request, queryset):
        """ Добавление в раздел actions административной панели, Опубликовано """
        count_published = queryset.update(posted_by=True)
        if count_published == 1:
            message_published = '1 запись опубликована'
        else:
            message_published = f'{count_published} записей опубликовано'
        self.message_user(request, message_published)

    def not_published(self, request, queryset):
        """ Добавление в раздел actions административной панели, Не опубликовано """
        count_published = queryset.update(posted_by=False)
        if count_published == 1:
            message_published = '1 запись снята с публикации'
        else:
            message_published = f'{count_published} записей сняты с публикации'
        self.message_user(request, message_published)

    published.short_description = 'Опубликовать выбранные записи'
    not_published.short_description = 'Снять с публикации выбранные записи'


admin.site.site_header = "Администрирование сайта"
admin.site.site_title = "Адимнистрирование сайта"
