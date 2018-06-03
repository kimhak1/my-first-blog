from django.shortcuts import render
from customuser.forms import CustomUserRegisterForm, CustomUserLoginForm, SignForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import CustomUser
from django.contrib.auth.models import User

def sign(request):
    if request.method == "POST":
        form = SignForm(request.POST)
        if form.is_vaild():
            # **사전변수 : 사전에 들어있는 모든 키:값을 매개변수로 넘겨줌
            #User.objects.create_user() : dJango의 User모델클래스에서
            #자동으로 회원을 생성함
             new_user = User.objects.create_user(**form.cleaned_data)
             return HttpResponseRedirect(reverse('polls:index'))
    elif request.method == "GET":
        form = SignForm()
        return render(request, "customuser/sign.html",{'form':form})
'''
def sign(request):
    if request.method=="POST":
        obj = CustomUserRegisterForm(request.POST)
        if obj.is_valid():
            id = obj.cleaned_data['id']
            password = obj.cleaned_data['password']
            passwordCheck = obj.cleaned_data['passwordCheck']
            if password == passwordCheck:
                makeUser, find = CustomUser.objects.get_or_create(id=id)
                if find:
                    makeUser.password=password
                    makeUser.save()
                    return HttpResponseRedirect( reverse('polls:index') )
                else:
                    error='같은 이름의 아이디가 존재합니다.'
                
                try:
                    user = CustomUser.objects.get(id=id)
                except CustomUser.DoesNotExist:
                    makeUser = CustomUser()
                    makeUser.id = id
                    makeUser.password = password
                    makeUser.save()
                    return HttpResponseRedirect( reverse('polls:index') )
                
                
                
            else:
                error = '비밀번호가 맞지 않습니다.'
            return render(request, 'customuser/sign.html',{'form':obj, 'error':error})      
                
    elif request.method=="GET":
        obj = CustomUserRegisterForm()
        return render(request, 'customuser/sign.html',{'form':obj})
'''
def login(request):
    if request.method=="POST":
        obj = CustomUserLoginForm(request.POST)
        if obj.is_valid():
            id = obj.cleaned_data['id']
            password = obj.cleaned_data['password']
            user = CustomUser.objects.filter(id=id).filter(password=password)
            if user.exists():
                request.session['loginstate']=True
                request.session['username']=user[0].id
                return HttpResponseRedirect( reverse('polls:index') )
            else:
                pass 
        else:
            pass
    elif request.method=="GET":
        obj = CustomUserLoginForm()
        return render(request, 'customuser/login.html', {'form':obj })
    
def logout(request):
    request.session.flush()
    return HttpResponseRedirect( reverse('polls:index') )