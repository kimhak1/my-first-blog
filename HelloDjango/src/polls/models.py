from django.db import models
from customuser.models import CustomUser 
# Create your models here.
class Question(models.Model):
    #id는 생략해도자동으로 장고에서 만들어줌
    question_text = models.CharField('질문 제목', max_length=200)
    pub_date = models.DateTimeField('date published')
    customuser = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    image = models.ImageField('이미지 파일',upload_to='uploadfile/%Y/%m/%d/content',blank=True,null=True,)
    def __str__(self):
        return self.question_text
    
class Choice(models.Model):
    choice_text = models.CharField('답변', max_length=100)
    votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.choice_text
    
    
class Comment(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    customuser = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    text = models.TextField('댓글')
    image = models.ImageField('이미지', upload_to='comment/%Y/%m/%d/',blank=True,null=True,)
    
    
    
    
    
    
    
    
    