from django import forms
from .models import Post


# Можно я скажу прямо? Спринт - говнище, теорию объясняют вразброс.
# Нахрена мне объяснять про области видимости и декораторы В ТЕМЕ ПРО ДЖАНГО???
# Нахрена мне пихать упражнения, которые не имеют привязки к проекту???
# НАХРЕНА НУЖЕН ЭТОТ СРАНЫЙ ТРЕНАЖЁР??? ЧТОБЫ УБИТЬ НЕРВНЫЕ КЛЕТКИ?!?!?!
# Я проходил туториалы на ютубе от Кори Шафера, у меня рабочий сайт вышел
# за три дня и 12 видео. Тут я бодаюсь с теорией две недели.
# У меня уже сил нет, Яндекс нихрена не умеет ни объяснять теорию, ни адекватно
# настраивать автотесты. Пришлось учиться по ютубу и стаковерфлоу.
# Все силы высосаны. Надеюсь, за день с твоими правками справлюсь и код
# не как у косорукой макаки-дауна.

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        exclude = ('author',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_text(self):
        data = self.cleaned_data['text']
        if len(data) < 11:
            raise forms.ValidationError('Текст публикации не может быть короче'
                                        ' 10 символов.')
        return data
