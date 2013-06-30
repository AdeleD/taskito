from django import forms
from django.forms import ModelForm
from models import Task, Comment


class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'allow_comments']


class UpdateTaskForm(ModelForm):
    progress = forms.IntegerField(min_value=0, max_value=100, help_text="An integer between 0 and 100")

    class Meta:
        model = Task
        fields = ['name', 'description', 'allow_comments', 'progress']


class AuthenticatedCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 30}),
        }


class AnonymousCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['user_name', 'user_email', 'content']
