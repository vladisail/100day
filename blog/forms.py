from django import forms
from .models import Post, Comment


# Класс формы добавления поста
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')
        widgets = {
            'body': forms.Textarea(attrs={'rows': 10, 'cols': 60, 'placeholder': 'Напишите свой пост'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body_comment']  # Поля, которые должны быть в форме (в данном случае, только текст комментария)
        widgets = {
            'body_comment': forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': 'Введите ваш комментарий здесь...'})
        }
        labels = {
            'body_comment': '',  # Устанавливаем пустую строку в качестве метки
        }