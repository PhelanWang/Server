from django.conf.urls import url

from . import views

# from .views import CategoryViewSet, EntryViewSet, UserViewSet

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^categorys/$', views.CategoryList.as_view()),
    url(r'^categorys/(?P<pk>[0-9]+)/$', views.CategoryDetail.as_view()),

    url(r'^entrys/(?P<pk>[0-9]+)/$', views.EntryList.as_view()),
    url(r'^entry/(?P<pk>[0-9]+)/$', views.EntryDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)






