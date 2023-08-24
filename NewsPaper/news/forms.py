from django import forms
from .models import Post, User, Category, Author

class PostForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), label="Автор")
    heading = forms.CharField(label="Заголовок")
    text = forms.CharField(label="Текст", widget=forms.Textarea)
    post_category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), label="Категория")

    class Meta:
        model = Post
        fields = [
            'author',
            'heading',
            'text',
            'post_category',
        ]