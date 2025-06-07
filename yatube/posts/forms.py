from django import forms  # Импортируем модуль forms, из него возьмём класс ModelForm

from .models import Post  # Импортируем модель, чтобы связать с ней форму


class PostForm(forms.ModelForm):
    class Meta:
        # Эта форма будет работать с моделью Post
        model = Post

        # Здесь перечислим поля модели, которые должны отображаться в веб-форме;
        # при необходимости можно вывести в веб-форму только часть полей из модели.
        fields = ('text', 'group')

    def clean_text(self):
        data = self.cleaned_data['text']

        # Если пользователь не поблагодарил администратора - считаем это ошибкой
        if data == '':
            raise forms.ValidationError('Вы обязательно должны заполнить поле')

        # Метод-валидатор обязательно должен вернуть очищенные данные,
        # даже если не изменил их
        return data
