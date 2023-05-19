from django.shortcuts import render
from article.models import Work
# Create your views here.
def article_get_by_name(article_name):
    return Work.objects.filter(work_name__icontains=article_name)

def article_get_by_id(article_id):
    return Work.objects.filter(id=article_id)

def article_get_by_author(in_author):
    return Work.objects.filter(author__icontains=in_author)
