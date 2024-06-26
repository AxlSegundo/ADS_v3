from django import forms
from .models import Calificacion

class CalificacionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar el widget del campo id_alumno para mostrar el nombre del alumno
        self.fields['id_alumno'].widget = forms.Select(choices=self.get_alumnos_choices())

    def get_alumnos_choices(self):
        # Obtener las opciones (choices) para el campo id_alumno como pares (id, nombre)
        return [(alumno.id, f"{alumno.nombre} {alumno.apellidoPat} {alumno.apellidoMat}") for alumno in self.fields['id_alumno'].queryset]

    class Meta:
        model = Calificacion
        exclude = ['id', 'id_profesor']