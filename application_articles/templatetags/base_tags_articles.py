from django import template
from django.db.models import Count, F

from application_articles.models import Section, Category, Subject

register = template.Library()


@register.simple_tag()
def get_section():
    """Получение разделов, использование в header_navigation.html"""
    """Getting partitions, using in header_navigation.html"""
    section = Section.objects.annotate(cnt=Count('article')).filter(cnt__gt=0)
    return section


@register.simple_tag()
def get_category(active_section=''):
    """Получение разделов, использование в content_navigation.html"""
    """Getting partitions, using in content_navigation.html"""

    if active_section == '':
        categories = Category.objects.annotate(cnt=Count('article', filter=F('article__posted_by'))).filter(
            cnt__gt=0)
    else:
        categories = Category.objects.filter(article__section__title=active_section.title).annotate(
            cnt=Count('article', filter=F('article__posted_by'))).filter(cnt__gt=0)
    return categories


@register.simple_tag()
def get_subjects(active_section='', active_category=''):
    """Получение разделов, использование в content_navigation.html"""
    """Getting partitions, using in content_navigation.html"""

    if active_section == '' and active_category == '':
        subjects = Subject.objects.annotate(
            cnt=Count('article', filter=F('article__posted_by'))).filter(cnt__gt=0)
    else:
        subjects = Subject.objects.filter(article__section__title=active_section.title,
                                          article__category__title=active_category.title).annotate(
            cnt=Count('article', filter=F('article__posted_by'))).filter(cnt__gt=0)

    return subjects
