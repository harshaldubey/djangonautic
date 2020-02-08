from django.shortcuts import render, redirect
from .models import Article
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
from django.contrib import messages

# Create your views here.
def article_list(request):
    if (request.method == 'POST'): # if user delete article
        delete_slug = request.POST.get("delete_slug")
        article = Article.objects.get(slug=delete_slug)
        article.delete()
    articles = Article.objects.all().order_by('date')
    return render(request, "article_list.html", {'articles' : articles})

def article_slug(request, slug):
    #return HttpResponse(slug)
    try:
        article = Article.objects.get(slug=slug)
        comments = article.comment_set.all()
        if request.method == 'POST':
            form = forms.AddComment(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.article = article
                comment.save()
                return redirect("articles:slug", slug=slug)

            user = request.user
        else:
            form = forms.AddComment()
        return render(request, "article_detail.html", {'article' : article, 'form' : form, 'comments' : comments})
    except:
        return redirect("articles:list")

@login_required(login_url='accounts:login')
def article_create(request):
    if (request.method == 'POST'):
        if Article.objects.filter(slug=request.POST.get("slug")).exists():
            form = forms.CreateArticle()
            messages.error(request, "This article title(slug) is exists!!")
            return render(request, 'article_create.html', {'form' : form})
        form = forms.CreateArticle(request.POST, request.FILES)
        if (form.is_valid()):
            # save article to DB
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect("articles:list")
    form = forms.CreateArticle()
    return render(request, 'article_create.html', {'form' : form})