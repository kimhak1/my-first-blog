from django.forms.models import ModelForm
from .models import Post,Image

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('pub_date', 'author',)
    def __init__(self, *args, **kwargs):
        super(PostForm,self).__init__(*args,**kwargs)
        self.fields['type'].empty_label=None
class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields=('post','image',)
        