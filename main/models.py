# main/models.py
from django.db import models

class Alumno(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nombre = models.TextField()
    apellidoPat = models.TextField()
    apellidoMat = models.TextField()
    password = models.TextField()

class Profesor(models.Model):
    id = models.CharField(primary_key=True,max_length=100)
    nombre = models.TextField()
    apellidoPat = models.TextField()
    apellidoMat = models.TextField()
    password = models.TextField()

class Materia(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.TextField()
    semestre = models.IntegerField()
    
    def __str__(self):
        return self.nombre

class Horario(models.Model):
    nombre_mat = models.ForeignKey(Materia, on_delete=models.CASCADE)
    dia = models.CharField(max_length=10, choices=[
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes')
    ])
    hora_inicio = models.CharField(max_length=10)
    hora_fin = models.CharField(max_length=10)

class Calificacion(models.Model):
    PARCIAL_CHOICES = [
        (1, 'Parcial 1'),
        (2, 'Parcial 2'),
        (3, 'Parcial 3'),
        (4, 'Final'),  # Calificación final promediada de los tres parciales
    ]
    
    id = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    id_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    id_materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    cal = models.FloatField()
    parcial = models.IntegerField(choices=PARCIAL_CHOICES, default=4)

class Grupos(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre_mat = models.ForeignKey(Materia, on_delete=models.CASCADE)
    id_profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)

    def __str__(self):
        return f"Grupo de {self.nombre_mat} con {self.id_profesor}"

class TipoCal(models.Model):
    semestre = models.ForeignKey(Materia, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete= models.CASCADE)
    def __str__(self):
        return f"{self.alumno.nombre} - {self.semestre.nombre}"
    
class RelacionGrupoAlumno(models.Model):
    alumno = models.ForeignKey('Alumno', on_delete=models.CASCADE)
    grupo = models.ForeignKey('Grupos', on_delete=models.CASCADE)
    materia = models.ForeignKey('Materia', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.alumno.nombre} - {self.grupo.nombre_mat.nombre}"