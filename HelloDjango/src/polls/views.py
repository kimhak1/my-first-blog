from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from polls.models import Question, Choice
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from polls.forms import ChoiceForm,QuestionForm,CommentForm
from customuser.models import CustomUser 

# Create your views here.
def index(request):
    data = Question.objects.all()
    return render(request, 'polls/index.html', {'data':data})
    # return HttpResponse('응답 완료')

def detail(request, question_id):
    if request.method == "GET":
        question_data = get_object_or_404(Question,pk=question_id)
        form = CommentForm()
        # choice_data = Choice.objects.filter(question=question_id)
        context = {
                'form' : form,
                'question_data':question_data,
                # 'choice_data':choice_data
        }
        return render(request, 'polls/detail.html', context)
        # return HttpResponse('question_id : {}'.format(question_id))
    elif request.method == "POST":
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            question = get_object_or_404(Question,pk=question_id)
            customuser = get_object_or_404(CustomUser,pk=request.session['username'])
            obj = form.save(commit=False)
            obj.question = question
            obj.customuser = customuser
            obj.save()
            return HttpResponse( reverse('polls:detail', args=(question_id, )))

from django.db.models import F
 
def vote(request, question_id):
    if request.method =="POST":
        data = Choice.objects.get(id=request.POST.get('vote'), question=question_id)
        data.votes = F('votes') + 1
        data.save()
    
        return HttpResponseRedirect( reverse('polls:results',args=(question_id, ) ) )
    else:
        return HttpResponseRedirect( reverse('polls:detail', args=(question_id, )))
    
    # return redirect('/polls/{}/results/'.format(question_id))

def results(request, question_id):
    data = Question.objects.get(id=question_id)
    context = {
        'data':data
    }
    return render(request, 'polls/results.html', context)
    # return HttpResponse('question_id : {}'.format(question_id))
    
def registerQ(request):
    if request.session['loginstate'] == True:
        if request.method =="GET":
            obj = QuestionForm()
            return render(request, 'polls/registerQ.html', {'form' : obj })
        else:
            obj = QuestionForm(request.POST,request.FILES)
            
            if obj.is_valid():
                user = get_object_or_404(CustomUser, pk = request.session['username'])
                
                question = obj.save(commit=False)
                question.pub_date = datetime.now()
                question.customuser = user
                question.save()
                return HttpResponseRedirect(reverse('polls:index'))
            else:
                return render(request, 'polls/registerQ.html', 
                              {'form' : obj, 'error_message' : "비정상적인 값입니다."})
    else:
        return render(request,'polls/error.html', {'error': '로그인 후 접근할 수 있는 페이지입니다.'})
        
        
def registerC(request,question_id):
    if not 'username' in request.session:
        return render(request, 'polls/error.html',{'error':'로그인 후 접근할 수 있는 페이지 입니다.'})
    question = get_object_or_404(Question,pk=question_id)
    if question.customuser.id == request.session['username']:
        if request.method =="GET":
            obj = ChoiceForm()
            return render(request, 'polls/registerC.html', {'form' : obj }, {'question' : question})
        else:
            obj = ChoiceForm(request.POST)
            
            if obj.is_valid():
                choice = obj.save(commit=False)
                choice.question = question
                choice.save()
                return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))
            else:
                return render(request, 'polls/registerC.html', 
                              {'form' : obj, 'error_message' : "비정상적인 값입니다."})
    else:
        return render(request, 'polls/error.html', {'error': '본인이 작성한 글이 아닙니다.'})            
    

def deleteQ(request, question_id):
    if not 'username' in request.session:
        return render(request, 'polls/error.html',{'error':'로그인 후 접근할 수 있는 페이지 입니다.'})
    obj = get_object_or_404(Question,pk=question_id)
    if obj.customuser.id == request.session[ 'username' ]:
        obj.delete()
        return HttpResponseRedirect( reverse('polls:index'))
    else:
        return render(request, 'polls/error.html', {'error':'본인이 작성한 글만 삭제할 수 있습니다.'})

def deleteC(request, choice_id):
    if not 'username' in request.session:
        return render(request, 'polls/error.html',{'error':'로그인 후 접근할 수 있는 페이지 입니다.'})
    obj = get_object_or_404(Choice,pk=choice_id)
    if obj.customuser.id == request.session[ 'username' ]:
        question_id = obj.question.id
        obj.delete()
        return HttpResponseRedirect( reverse('polls:detail', args=(question_id, )))
    else:
        return render(request, 'polls/error.html', {'error':'본인이 작성한 글만 삭제할 수 있습니다.'})
    
def search(request):
    type = request.GET.get('type','0')
    content = request.GET.get('content', '' )
    if type == '0':
        q = Question.objects.filter(question_text__contains = content)
        return render(request, 'polls/search.html', {'resultlist' : q, 'content' : content})
    
    elif type == '1':
        user = CustomUser.objects.filter(id=content)
        q = Question.objects.filter(customuser__in=user)
        return render(request, 'polls/search.html', {'resultlist':q, 'content':content})
    elif type == '2':
        content = int(content)
        q = Choice.objects.filter(votes__gt=content)
        return render(request, 'polls/searchC.html', {'resultlist':q, 'content':content})
    else: 
        return render(request, 'polls/error.html', { 'error': '검색 타입이 정상적이지 않습니다.'})
        
    
    
    
    
    
    
    
    