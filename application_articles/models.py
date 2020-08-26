from django.db import models
from django.urls import reverse


class Section(models.Model):
    """Модель разделов"""
    title = models.CharField(max_length=69, verbose_name="Название")
    slug = models.SlugField(max_length=69, unique=True, verbose_name="URL")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('sections', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ['title']


class Category(models.Model):
    """Модель категорий"""
    title = models.CharField(max_length=69, verbose_name="Название")
    slug = models.SlugField(max_length=69, unique=True, verbose_name="URL")

    def __str__(self):
        return self.title + " (" + self.slug + " )"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['title']


class Subject(models.Model):
    """Модель тем"""
    title = models.CharField(max_length=69, verbose_name="Название")
    slug = models.SlugField(max_length=69, unique=True, verbose_name='URL')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
        ordering = ['title']


class Article(models.Model):
    """Модель статей"""
    title = models.CharField(max_length=69, verbose_name="Заголовок")
    slug = models.SlugField(max_length=69, unique=True, verbose_name='URL')
    section = models.ForeignKey(
        'Section', on_delete=models.CASCADE, verbose_name="Раздел")
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, verbose_name="Категория")
    subject = models.ForeignKey(
        'Subject', on_delete=models.CASCADE, verbose_name="Тема")
    content_description = models.TextField(
        max_length=700, verbose_name="Описание статьии")
    content = models.TextField(blank=True, verbose_name="Статья")
    publication_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации")
    update_date = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления")
    image_publication = models.ImageField(
        upload_to="img/%Y/%d-%m", verbose_name="Изображение")
    posted_by = models.BooleanField(default=False, verbose_name="Опубликовано")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles', kwargs={'section_slug': self.section.slug, 'category_slug': self.category.slug, 'subject_slug': self.subject.slug, 'slug': self.slug})

    def get_subject_url(self):
        return reverse('subjects', kwargs={'section_slug': self.section.slug, 'category_slug': self.category.slug, 'slug': self.subject.slug})
    
    def get_category_url(self):
        return reverse('categories', kwargs={'section_slug': self.section.slug, 'slug': self.category.slug})
    
    def get_section_url(self):
        return reverse('sections', kwargs={'slug': self.section.slug})

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьии"
        ordering = ['-publication_date']
