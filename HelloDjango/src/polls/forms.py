'''
Created on 2018. 5. 20.

@author: 1104-5
'''
#모델클래스와 관련된 입력양식 클래스를 만드는 파일
from django.forms.models import ModelForm
from . import models

class QuestionForm(ModelForm):
    class Meta:
        model = models.Question
        fields = ['question_text' ,'image',]

class ChoiceForm(ModelForm):
    class Meta:
        model = models.Choice
        #fields = ['choice_text', 'question',]
        exclude = ['votes', 'question', ]

class CommentForm(ModelForm):
    class Meta:
        model = models.Comment
        #fields = ['choice_text', 'question',]
        fields = ['text', 'image', ]
        
        
        
        
        