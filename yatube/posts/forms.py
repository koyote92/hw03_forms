from django import forms
from .models import Post

TEXT_LENGTH_MINIMAL = 10


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        exclude = ('author',)
        # help_text добавил в models.py

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_text(self):
        data = self.cleaned_data['text']
        if len(data) < TEXT_LENGTH_MINIMAL:
            raise forms.ValidationError('Текст публикации не может быть короче'
                                        ' 10 символов.')
        return data
