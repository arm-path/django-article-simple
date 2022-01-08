from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from slugify import slugify

from .forms import SectionForm, CategoryForm, SubjectForm, ArticleForm, UserRegistration, UserAuthorization, Feedback
from .models import Section, Category, Subject, Article


class SectionList(ListView):
    """ Представление разделов """
    model = Article
    template_name = 'application_articles/sections.html'
    context_object_name = 'articles'
    paginate_by = 3
    allow_empty = False

    def get_context_data(self, object_list=None, *args, **kwargs):
        """ Добавление дополнительного контекста к представлению разделов """
        context = super().get_context_data(**kwargs)
        context['get_section_view'] = Section.objects.annotate(cnt=Count('article')).get(slug=self.kwargs['slug'])
        context['articles_sections'] = context['articles']
        context['active_link_section'] = 'active_link'
        return context

    def get_queryset(self):
        """Получение статей раздела"""
        return Article.objects.filter(
            section_id=Section.objects.get(slug=self.kwargs['slug']),
            posted_by=True
        ).select_related('section', 'category', 'subject', )


class CategoryList(ListView):
    """Представление категорий"""
    model = Article
    template_name = 'application_articles/categories.html'
    context_object_name = 'articles'
    paginate_by = 3
    allow_empty = False

    def get_context_data(self, object_list=None, *args, **kwargs):
        """Добавление дополнительного контекста к представлению категорий"""
        context = super().get_context_data(**kwargs)
        context['get_section_view'] = Section.objects.get(slug=self.kwargs['section_slug'])
        context['get_category_view'] = Category.objects.get(slug=self.kwargs['slug'])
        context['articles_sections'] = Article.objects.filter(section_id=context['get_section_view']
                                                              ).select_related('section', 'category')
        context['active_link_section'] = 'active_link'
        context['active_link_category'] = 'active_link'

        return context

    def get_queryset(self):
        """Получение статей раздела и категорий"""
        return Article.objects.filter(
            section_id=Section.objects.get(slug=self.kwargs['section_slug']),
            category_id=Category.objects.get(slug=self.kwargs['slug']), posted_by=True
        ).select_related('section', 'category', 'subject')


class SubjectList(ListView):
    """Представление тем"""
    model = Article
    template_name = "application_articles/subjects.html"
    context_object_name = 'articles'
    paginate_by = 3
    allow_empty = False

    def get_context_data(self, object_list=None, *args, **kwargs):
        """Добавление дополнительного контекста к представлению тем"""
        context = super().get_context_data(**kwargs)
        context['get_section_view'] = Section.objects.get(slug=self.kwargs['section_slug'])
        context['get_category_view'] = Category.objects.get(slug=self.kwargs['category_slug'])
        context['get_subject_view'] = Subject.objects.get(slug=self.kwargs['slug'])
        context['articles_sections'] = Article.objects.filter(section_id=context['get_section_view']
                                                              ).select_related('section', 'category')
        context['articles_sections_categories'] = Article.objects.filter(section_id=context['get_section_view'],
                                                                         category_id=context['get_category_view'],
                                                                         posted_by=True
                                                                         ).select_related('section', 'category',
                                                                                          'subject')
        context['active_link_section'] = 'active_link'
        context['active_link_subject'] = 'active_link'
        context['active_link_category'] = 'active_link'
        return context

    def get_queryset(self):
        """Получение статей раздела, категорий и тем"""
        return Article.objects.filter(section_id=Section.objects.get(slug=self.kwargs['section_slug']),
                                      category_id=Category.objects.get(slug=self.kwargs['category_slug']),
                                      subject_id=Subject.objects.get(slug=self.kwargs['slug']),
                                      posted_by=True
                                      ).select_related('section', 'category', 'subject')


class ArticleList(ListView):
    """Представление статей, начальная страница"""
    model = Article
    template_name = 'application_articles/base.html'
    context_object_name = 'articles'
    paginate_by = 3

    def get_context_data(self, object_list=None, *args, **kwargs):
        """Добавление дополнительного контекста к представлению списка статей"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список статей'
        return context

    def get_queryset(self):
        """Получение списка статей"""
        context = Article.objects.filter(posted_by=True)
        return context


class ArticleDetail(DetailView):
    """Представление статьии"""
    model = Article
    template_name = 'application_articles/articles.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        """Добавление дополнительного контекста к представлению статьии"""
        context = super().get_context_data(**kwargs)
        context['sections'] = self.kwargs['section_slug']
        context['get_section_view'] = Section.objects.get(slug=self.kwargs['section_slug'])
        return context


class SectionCreate(LoginRequiredMixin, CreateView):
    """Добавление раздела"""
    form_class = SectionForm
    template_name = 'application_articles/forms.html'
    login_url = 'initial'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link_section'] = 'active_link'
        context['title'] = 'Добавление раздела'
        return context

    def post(self, request, *args, **kwargs):
        """Переопределение метода post, для построения поля slug"""
        form = SectionForm(request.POST)
        form_post = form.save(commit=False)
        form_post.slug = slugify(form_post.title)
        form_post.save()
        return redirect('add_article')


class CategoryCreate(LoginRequiredMixin, CreateView):
    """Добавление категории"""
    form_class = CategoryForm
    template_name = 'application_articles/forms.html'
    login_url = 'initial'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_link_category'] = 'active_link'
        context['title'] = 'Добавление категории'
        return context

    def post(self, request, *args, **kwargs):
        """Переопределение метода post, для построения поля slug"""
        form = CategoryForm(request.POST)
        form_post = form.save(commit=False)
        form_post.slug = slugify(form_post.title)
        form_post.save()
        return redirect('add_article')


class SubjectCreate(LoginRequiredMixin, CreateView):
    """Добавление темы"""
    form_class = SubjectForm
    template_name = 'application_articles/forms.html'
    success_url = reverse_lazy('add_subject')
    login_url = 'initial'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление темы'
        context['active_link_subject'] = 'active_link'
        return context

    def post(self, request, *args, **kwargs):
        """Переопределение метода post, для построения поля slug"""
        form = SubjectForm(request.POST)
        form_post = form.save(commit=False)
        form_post.slug = slugify(form_post.title)
        form_post.save()
        return redirect('add_article')


class ArticleCreate(LoginRequiredMixin, CreateView):
    """Добавление статьии"""
    form_class = ArticleForm
    template_name = 'application_articles/forms.html'
    success_url = reverse_lazy('add_article')
    login_url = 'initial'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьии'
        context['active_link_article'] = 'active_link'
        return context

    def post(self, request, *args, **kwargs):
        """Переопределение метода post, для построения поля slug"""
        form_data = ArticleForm(request.POST, files=request.FILES)
        # files=request.FILES - Изображение
        # Не забыть в форме добавить enctype="multipart/form-data"
        if form_data.is_valid():
            form_post = form_data.save(commit=False)
            form_post.slug = slugify(form_post.title)
            form_post.save()
            messages.success(request, 'Статья успешно добавлена, ожидайте подтверждения администратором сайта')
        else:
            messages.success(request, 'Ошибка добавления статьии, пожалуйста перепроверьте вводимые данные')
        return redirect('add_article')


def registration(request):
    """Форма регистрации пользователя"""
    if request.method == "POST":
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('authorization')
        else:
            messages.error(request, 'Вы не прошли регистрацию')
    else:
        form = UserRegistration()
    return render(request, 'application_articles/registration.html', {'form': form})


def authorization(request):
    """Форма авторизации пользователя"""
    if request.method == "POST":
        form = UserAuthorization(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('initial')
    else:
        form = UserAuthorization()
    return render(request, 'application_articles/authorization.html', {'form': form})


def logout_view(request):
    """Форма выхода из системы пользователя"""
    logout(request)
    return redirect('authorization')


def feedback(request):
    """Представление обратной связи"""
    if request.method == "POST":
        form = Feedback(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['title'], form.cleaned_data['content'],
                             'TODO: Указать электронную почту отправителя',
                             ['TODO: Указать электронные почты получателей', ], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо успешно отправлено')
                return redirect('feedback')
            else:
                messages.error(request, 'Не удалось отправить письмо')
    else:
        form = Feedback()
    return render(request, 'application_articles/feedback.html', {'form': form})
