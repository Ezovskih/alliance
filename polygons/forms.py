from django import forms
from django.contrib.gis.geos import GEOSGeometry

from .models import PolygonModel


class PolygonForm(forms.ModelForm):
    class Meta:
        model = PolygonModel
        fields = ('name', 'shape')
        widgets = {
            'shape': forms.HiddenInput(),
        }

    coordinates = forms.CharField(
        label="Координаты (широта, долгота)",
        widget=forms.Textarea(attrs={'rows': '6'}),
    )

    def clean_shape(self):
        shape_data = self.cleaned_data['shape']
        try:
            return GEOSGeometry(shape_data)
        except:
            raise forms.ValidationError("Некорректные координаты полигона!")
