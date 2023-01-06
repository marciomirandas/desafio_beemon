from django import forms
import datetime


class IndexForm(forms.Form):

    date = forms.DateField(label='Data',widget=forms.TextInput(attrs={'title': 'Data','class': 'form-control', 'type':'date', 'style':'max-width: 400px;', 'required': True}))
    time = forms.TimeField(label='Hora',widget=forms.TextInput(attrs={'title': 'Hora','class': 'form-control', 'type':'time', 'style':'max-width: 400px;', 'required': True}))
    

    class Meta:
        fields = ['date', 'time']
        

    def clean_date(self):
        date = self.cleaned_data.get('date')

        if date < datetime.date.today():
            raise forms.ValidationError('Erro! Essa data já passou!')

        return date


    