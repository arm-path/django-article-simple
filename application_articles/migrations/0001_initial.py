# Generated by Django 3.0.7 on 2020-08-26 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=69, verbose_name='Название')),
                ('slug', models.SlugField(max_length=69, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=69, verbose_name='Название')),
                ('slug', models.SlugField(max_length=69, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Разделы',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=69, verbose_name='Название')),
                ('slug', models.SlugField(max_length=69, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Тема',
                'verbose_name_plural': 'Темы',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=69, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=69, unique=True, verbose_name='URL')),
                ('content_description', models.TextField(max_length=700, verbose_name='Описание статьии')),
                ('content', models.TextField(blank=True, verbose_name='Статья')),
                ('publication_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('image_publication', models.ImageField(upload_to='img/%Y/%d-%m', verbose_name='Изображение')),
                ('posted_by', models.BooleanField(default=False, verbose_name='Опубликовано')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application_articles.Category', verbose_name='Категория')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application_articles.Section', verbose_name='Раздел')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application_articles.Subject', verbose_name='Тема')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьии',
                'ordering': ['-publication_date'],
            },
        ),
    ]
