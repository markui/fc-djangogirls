from django.http import HttpResponse
from django.shortcuts import render
from .models import Post

# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    context = {
        # posts key의 value는 QuerySet
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context)
    # 단순 html파일이 아니다. -> template언어를 장고 내부에서 사용해 html 파일을 렌더링해서 사용자 요청에 대해 보내주는 것