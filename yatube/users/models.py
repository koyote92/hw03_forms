from django.db import models


# Вот тут я твой коммент вообще не понял, это было в теории и я добавил,
# хотя сам не понимаю, нахрена оно в этом проекте тут
class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Электронная почта')
    subject = models.CharField(max_length=100, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Текст письма')
    is_answered = models.BooleanField(default=False)
