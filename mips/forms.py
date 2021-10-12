from django import forms

class BytesField(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3,
        'placeholder': 'Введите набор байт или выберите готовый пример из списка'
    }))