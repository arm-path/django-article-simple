from django.urls import path

from .views import SectionCreate, CategoryCreate, SubjectCreate, ArticleCreate
from .views import SectionList, CategoryList, SubjectList, ArticleList, ArticleDetail
from .views import registration, authorization, logout_view, feedback

urlpatterns = [
    path('', ArticleList.as_view(), name='initial'),
    path('section/<slug:slug>/', SectionList.as_view(), name="sections"),
    path('section/<section_slug>/category/<slug:slug>/', CategoryList.as_view(), name="categories"),
    path('section/<section_slug>/category/<category_slug>/subject/<slug:slug>/', SubjectList.as_view(), name="subjects"),
    path('article/<section_slug>/<category_slug>/<subject_slug>/<slug:slug>/', ArticleDetail.as_view(), name='articles'),

    path('add-section/', SectionCreate.as_view(), name='add_section'),
    path('add-category/', CategoryCreate.as_view(), name="add_category"),
    path('add-subject/', SubjectCreate.as_view(), name="add_subject"),
    path('add-article/', ArticleCreate.as_view(), name="add_article"),

    path('registration/', registration, name="registration"),
    path('authorization/', authorization, name="authorization"),
    path('logout/', logout_view, name="logout_view"),
    path('feedback/', feedback, name="feedback"),

]
