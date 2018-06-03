from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    if request.method=="GET":
        index = int(request.GET.get('index', 0))
        
        objs = Post.objects.all()
        max = len(objs)
        print(index,max)
        data = None
        if index*10 < max:
            if index*10 + 9 < max:
                data = objs[index*10 : index*10+10]
                nextPage = index + 1
            else:
                data = objs[index*10 : ]
                nextPage = -1
        else:
            return render(request, "polls/error.html", {'error' : "요청한 페이지가 없습니다."})
        previousPage = index - 1
        return render(request, "blog/index.html", {'data':data, 'nextPage' : nextPage, 'previousPage' : previousPage})
        
    else:
        return render(request, "polls/error.html", {'error' : "잘못된 접근입니다."})
    
def detail(request, post_id):
    obj = get_object_or_404(Post, pk = post_id)
    return render(request, 'blog/detail.html', {'obj' : obj })

@login_required
def posting(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            for f in request.FILES.getlist('images'):
                image = Image(post = obj, image=f)
                image.save()
            for f in request.FILES.getlist('files'):
                file = File(post = obj, file = f)
                file.save()
            return HttpResponseRedirect( reverse('blog:detail', args=(obj.id,) ))
        else:
            return render(request, "blog/posting.html",{'form':form, 'error' : '유효하지 않은 데이터입니다.'})
    elif request.method == "GET":
        form = PostForm()
        return render(request,'blog/posting.html', {'form':form})
    
@login_required
def post_delete(request,post_id):
    obj = get_object_or_404(Post,pk=post_id)
    if request.user == obj.author:
        obj.delete()
        return HttpResponseRedirect(reverse('blog:index'))
    else:
        return render(request, 'polls/error.html', {'error':'본인이 작성한 글만 삭제할 수 있습니다.', 
                                                    'mainurl':reverse('blog:index')})

@login_required
def post_update(request,post_id):
    obj = get_object_or_404(Post,pk=post_id)
    if obj.author != request.user:
        return render(request, "polls/error.html", {'error':'자신이 작성한 글만 수정할 수 있습니다.', 
                      'mainrl': reverse('blog:index')})
    if request.method=="POST":
        form = PostForm(request.POST, instance = obj)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('blog:detail',args=(post.id, ) ))
        else:
            return render(request,"blog/update.html",{'form':form,'error':'유효하지 않음.'})
    elif request.method=="GET":
        form = PostForm(instance = obj)
        return render(request,'blog/update.html',{'form' : form})



    
    