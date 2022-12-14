from django.urls import path
from django.conf.urls import url
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    ArticleCreateView,
    NewsCreateView,
    ArticleDetailView,
    NewsDetailView,
    ArticleUpdateView,
    ArticleDeleteView,
    UserArticleListView,
   StudentPostListView,
    UserNewsListView,
    ViewArticleListView,
     ViewNewsListView,
  NewsDeleteView,
  NewsUpdateView,
    
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('afterlogin/', views.afterlogin, name='blog-index'),

    path('blog-home', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('userarticle/<str:username>', UserArticleListView.as_view(), name='user-article'),
    path('articleviewstud/', ViewArticleListView.as_view(), name='view-article-student'),
    path('newsviewstud/', ViewNewsListView.as_view(), name='view-news-student'),
    
    path('usernews/<str:username>', UserNewsListView.as_view(), name='user-news'),
    path('studentpost/',StudentPostListView.as_view(), name='student-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('article/new/', ArticleCreateView.as_view(), name='post-create-article'),
    path('news/new/', NewsCreateView.as_view(), name='post-create-news'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
     path('news/<int:pk>/update/', NewsUpdateView.as_view(), name='news-update'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news-delete'),
    path('media/Files/<int:pk>',PostDeleteView.as_view(),name='post-delete' ),
    path('search/',views.search,name='search' ),
    path('about/', views.about, name='blog-about'),



    url(r'^password/$', views.change_password, name='change_password'),
]
