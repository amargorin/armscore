from django import forms
from django.contrib.auth.models import User
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from .models import MemberCats, StartLists, Match, Members


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ('title', 'location', 'fo', 'date', 'gj', 'gs', 'table_count', 'contacts', 'hands', 'poster', 'public')
        labels = {'title': 'Название турнира', 'location': 'Место проведения', 'fo': 'Федеральный округ',
                 'date':'Дата проведения', 'gj': 'Главный судья', 'gs': 'Главный секретарь',
                  'table_count': 'Количество столов', 'contacts': 'Контактная информация', 'hands': 'На руках',
                  'poster': 'Афиша турнира', 'public': 'Показывать турнир всем'}
        widgets = {'date': forms.widgets.DateInput(attrs={'type': 'date', 'min': 1, 'placeholder': 'yyyy-mm-dd',
                                            'class': 'form-control'}), 'poster': forms.FileInput()}

    def __init__(self, *args, **kwargs):
        self.match_id = kwargs.pop("match_id", None)
        self.owner_id = kwargs.pop("owner_id", None)
        super(ScoreForm, self).__init__(*args, **kwargs)
        self.fields['gj'].required = False
        self.fields['gs'].required = False
        self.fields['date'].required = False
        self.fields['contacts'].required = False
        self.fields['poster'].required = False
        self.fields['public'].required = False

    def save(self, *args, **kwargs):
        inst = super(ScoreForm, self).save(commit=False)
        inst.match_id = self.match_id
        inst.owner_id = self.owner_id
        inst.save()
        return inst


class CategoryForm(forms.ModelForm):
    class Meta:
        model = MemberCats
        fields = ['age_category', 'group_category', 'weight_category', 'hand']
        labels = {'age_category': 'Возрастная группа', 'group_category': 'Категория',
                  'weight_category': 'Весовая категория', 'hand': 'Рука'}

    def __init__(self, *args, **kwargs):
        self.match_id = kwargs.pop("match_id", None)
        super(CategoryForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        inst = super(CategoryForm, self).save(commit=False)
        inst.match_id = self.match_id
        inst.save()
        return inst


class MembersForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ('surname', 'name', 'second_name', 'far_passport', 'team', 'rank', 'birthday', 'trener',
                  'fo', 'photo')
        labels = {'surname': 'Фамилия', 'name': 'Имя', 'second_name': 'Отчество',
                  'far_passport': 'Паспорт ФАР', 'team': 'Команда', 'rank': 'Спортивное звание',
                  'birthday': 'Дата рождения', 'trener': 'Тренер',
                  'fo': 'Федеральный округ', 'photo': 'Фотография'}
        widgets = {'birthday': forms.widgets.DateInput(attrs={'type': 'date', 'min': 1, 'placeholder': 'yyyy-mm-dd',
                                                          'class': 'form-control'})}  #,
                   # 'surname': forms.widgets.Input(attrs={'autocomlete': 'off'})}

    def __init__(self, *args, **kwargs):
        # self.match_id = kwargs.pop("match_id", None)
        # self.category_id = kwargs.pop("category_id", None)
        super(MembersForm, self).__init__(*args, **kwargs)
        self.fields['second_name'].required = False
        self.fields['far_passport'].required = False
        self.fields['team'].required = False
        self.fields['rank'].required = False
        self.fields['birthday'].required = False
        self.fields['trener'].required = False
        self.fields['fo'].required = False
        self.fields['photo'].required = False

    def save(self, *args, **kwargs):
        inst = super(MembersForm, self).save(commit=False)
        # inst.match_id = self.match_id
        # inst.category_id = self.category_id

        inst.save()
        return inst
