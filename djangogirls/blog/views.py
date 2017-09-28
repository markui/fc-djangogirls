from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Post

# User라는 Class를 받아온다.
User = get_user_model()


# Create your views here.

def post_list(request):
    # post_list view가 published_date가 존재하는 Post목록만 보여주도록 수정
    posts = Post.objects.filter(published_date__isnull=False)
    context = {
        # posts key의 value는 QuerySet
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context)
    # 단순 html파일이 아니다. -> template언어를 장고 내부에서 사용해 html 파일을 렌더링해서 사용자 요청에 대해 보내주는 것


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context)


def post_add(request):
    """
    숙제
    1. post_form.html에 checkbox를 추가
    # 이를 이용해서 publish여부를 결정
    #
    # Post 생성 완료 후(DB에 저장 후), post_list페이지로 이동
    # https://docs.djangoproject.com/ko/1.11/topics/http/shortcuts/#redirect
    # extra) 작성한 Post에 해당하는 post_detail페이지로 이동
    #
    # Post생성시 Post.objects.create()메서드 사용
    #
    # extra) Post delete 기능 구현
    # def post_delete(request, pk):
    #  (POST요청에서만 동작해야함
    # -> pk에 해당하는 Post를 삭제하고 post_list페이지로 이동
    :param request:
    :return:
    """

    # POST request일 때,
    if request.method == 'POST':

        # 제목, 내용을 채워넣었을 때
        if request.POST.get('title') and request.POST.get('content'):

            post = Post(
                author=User.objects.get(username='markkim'),
                title=request.POST.get('title'),
                content=request.POST.get('content'),
            )
            if request.POST.get('is_published'):
                post.publish()
            # post를 레코드에 저장한다(published_date 존재하는 상태로)
            else:
                post.save()
            return HttpResponseRedirect(reverse('post_detail', kwargs={'pk': post.pk}))
            # 아니면, redirect('post_detail', pk=post.pk)

        # 한 값이라도 빠졌을 때,
        else:
            # title이나 content값이 오지 않았을 경우에는 객체를 생성하지 않고 다시 작성페이지로 이동
            # extra) 작성페이지로 이동시 '값을 입력해주세요'라는 텍스트를 어딘가에 표시(render) - 팝업창 모듈로 띄우는 것도 해볼 수 있음
            # extra****) modal
            context = {
                'title': request.POST.get('title'),
                'content': request.POST.get('content'),
                'needs_content': True
            }
            return render(request, 'blog/post_form.html', context)

    elif request.method == 'GET':
        return render(request, 'blog/post_form.html')


def post_delete(request, pk):
    """
    extra) Post delete 기능 구현
    # def post_delete(request, pk):
    #  (POST요청에서만 동작해야함)
    # -> pk에 해당하는 Post를 삭제하고 post_list페이지로 이동
    :param request:
    :param pk:
    :return:
    """
    Post.objects.get(pk=pk).delete()
    return redirect('post_list')
