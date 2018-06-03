from django.db import models
from django.conf import settings

# Create your models here.
class Posttype(models.Model):
    name = models.CharField('구분',max_length=200)
    def __str__(self):
        return self.name
    
class Post(models.Model):
    type = models.ForeignKey(Posttype, on_delete=models.CASCADE)
    headline = models.CharField('제목', max_length=200)
    content = models.TextField('내용', blank=True, null=True)
    pub_date = models.DateField('날짜', auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.headline
    class Meta:
        ordering=('-id', )
        
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField('이미지파일', upload_to='images/%Y%m%d')
    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Image.self).delete(*args,**kwargs)
    def __str__(self):
        return self.post.headline
    
class File(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField('파일', upload_to='files/%Y%m%d')
    def delete(self, using=None, keep_parents=False):
        self.file.delete()
        super(File,self).delete(using,keep_parents)
    def __str__(self):
        return self.post.headline
    
    
    
    
    
