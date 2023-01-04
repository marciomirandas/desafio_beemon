from django import forms


class IndexForm(forms.Form):
    lat = forms.CharField(label='Latitude', widget=forms.TextInput(attrs={'title': 'Latitude em coordenadas decimais','class':'form-control', 'style':'max-width: 400px;', 'required': True}))
    
    lon = forms.CharField(label='Longitude', widget=forms.TextInput(attrs={'title': 'Longitude em coordenadas decimais','class':'form-control', 'style':'max-width: 400px;', 'required': True}))


    class Meta:
        fields = ['lat', 'lon']
        labels = {
            'lat': 'Insert a watercourse',
            'lon': 'Insert a watercourse',
        }


    def clean_lat(self):
        lat = self.cleaned_data.get('lat')

        if float(lat) < -90 or float(lat) > 90:
            raise forms.ValidationError('Erro')

        return lat


    def clean_lon(self):
        lon = self.cleaned_data.get('lon')

        if float(lon) < -180 or float(lon) > 180:
            raise forms.ValidationError('Erro')
            
        return lon