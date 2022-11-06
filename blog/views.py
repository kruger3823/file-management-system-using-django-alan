from django.shortcuts import render, get_object_or_404,redirect,HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post,Articles,News
from users import models
import operator
from django.urls import reverse_lazy
from django.contrib.staticfiles.views import serve

from django.db.models import Q


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def search(request):
    template='blog/home.html'

    query=request.GET.get('q')

    result=Post.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query))
    paginate_by=2
    context={ 'posts':result }
    return render(request,template,context)
   


def getfile(request):
   return serve(request, 'File')


def is_student(user):
    return user.groups.filter(name="STUDENT").exists()
def is_teacher(user):
    return user.groups.filter(name="TEACHER").exists()

def afterlogin(request):
    if is_student(request.user):
        return render(request, 'blog/student.html')
    if is_teacher(request.user):
        return render(request, 'blog/teacher.html')
    else:
        return redirect('login/')
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
class UserArticleListView(ListView):
    model = Articles
    template_name = 'blog/user_article.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'articles'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Articles.objects.filter(author=user).order_by('-date_posted')

class UserNewsListView(ListView):
    model = News
    template_name = 'blog/user_news.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return News.objects.filter(author=user).order_by('-date_posted')

class ViewArticleListView(ListView):
    model = Articles
    template_name = 'blog/stud_view_article.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'articles'
    paginate_by = 2

    def get_queryset(self):
        profilestu  = models.Profile.objects.get(user__id=self.request.user.id)
        try:
            dep = profilestu.department.id
        except:
            messages.info(self.request,"No Articles!")
            b = []
            return b
        teachers = models.Profile.objects.filter(department=dep)
        print(teachers,"iiiiii")
        teachlist =[]
        for i in teachers:
            teachlist.append(i.user.id)
        return Articles.objects.filter(author__groups=2,author__id__in=teachlist).order_by('-date_posted')
        
class ViewNewsListView(ListView):
    model = News
    template_name = 'blog/stud_view_news.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        profilestu  = models.Profile.objects.get(user__id=self.request.user.id)
        try:
            dep = profilestu.department.id
        except:
            messages.info(self.request,"No News!")
            b = []
            return b
        teachers = models.Profile.objects.filter(department=dep)
        print(teachers,"iiiiidwsdi")
        teachlist =[]
        for i in teachers:
            teachlist.append(i.user.id)
        print(teachlist)
        print(News.objects.filter(author__groups=2,author__id__in=teachlist).order_by('-date_posted'))
        return News.objects.filter(author__groups=2,author__id__in=teachlist).order_by('-date_posted')

class StudentPostListView(ListView):
    
    model = Post
    template_name = 'blog/student_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        # user = get_object_or_404(User, username=self.kwargs.get('username'))
        profileteacher  = models.Profile.objects.get(user__id=self.request.user.id)
        try:
            studs = models.Profile.objects.filter(department__id=profileteacher.department.id)
        except:
            messages.info(self.request, 'No Students Posts!')
            b = []
            return b
        stud_ids =[]
        for i in studs:
            stud_ids.append(i.user.id)
        return Post.objects.filter(author__groups=1,author__id__in=stud_ids).order_by('-date_posted')
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
class ArticleDetailView(DetailView):
    model = Articles
    template_name = 'blog/article_detail.html'
class NewsDetailView(DetailView):
    model = News
    template_name = 'blog/news_detail.html'
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Articles
    template_name = 'blog/article_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'blog/news_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Articles
    template_name = 'blog/article_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model =News
    template_name = 'blog/news_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Articles
    success_url = '/'
    template_name = 'blog/article_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    success_url = '/'
    template_name = 'blog/news_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
