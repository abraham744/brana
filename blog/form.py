from ckeditor.fields import RichTextField
from django import forms
from .models import Comment, Post, Category, Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            "body",
            "recipient",
            "photo"
        ]
class VideoForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}))
   
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(author=self.request.user)

    class Meta:
        model = Post
        fields = ('video','thumbnail','title','content','category')

class PhotoForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(author=self.request.user)

    class Meta:
        model = Post
        fields = ('photo', 'title','content' , 'category', )


class MemeForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(MemeForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(author=self.request.user)

    class Meta:
        model = Post
        fields = ('photo','meme_top','meme_bottom', 'title', 'category','content', )

class AlbumUpdateForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Category
        fields = ('name','photo')

class UpdateForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(UpdateForm,self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(author=self.request.user)

    class Meta:
        model = Post
        fields = ( 'photo', 'video','thumbnail','title', 'category','content',)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        text = forms.CharField(widget=RichTextField())
        fields = ('text',)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        text = forms.CharField(widget=RichTextField())
        fields = ('text',)
