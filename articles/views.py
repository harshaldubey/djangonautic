from django.shortcuts import render, redirect
from .models import Article
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms

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
        if request.method == 'POST':
            comment = request.POST.get('comment')
            #print(request.POST.get('comment'))
            # TODO: save a comment and display it to article detail
            user = request.user
            print(f'comment by {request.user} msg : {comment}')
            
        return render(request, "article_detail.html", {'article' : article})
    except:
        return redirect("articles:list")

@login_required(login_url='accounts:login')
def article_create(request):
    if (request.method == 'POST'):
        form = forms.CreateArticle(request.POST, request.FILES)
        if (form.is_valid()):
            # save article to DB
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect("articles:list")
    else:
        form = forms.CreateArticle()
    return render(request, 'article_create.html', {'form' : form})