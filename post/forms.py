from django import forms

from post.models import Post

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder':'add tags, separeted by commas'
        })
    )
    
    class Meta:
        model = Post
        fields = ("picture","caption", "tags")
