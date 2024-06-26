from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CalificacionForm
from django.http import HttpRequest
from .models import Alumno, Profesor,Materia,Calificacion, Grupos, TipoCal,Horario
def pagina_principal(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
    
        if role == 'on':  # Checkbox checked means Profesor
            user = Profesor.objects.filter(id=username, password=password).first()
            if user:
                request.session['user_id'] = user.id
                request.session['role'] = 'profesor'
                return redirect('profesores')
        else:  # Unchecked checkbox means Alumno
            user = Alumno.objects.filter(id=username, password=password).first()
            if user:
                request.session['user_id'] = user.id
                request.session['role'] = 'alumno'
                return redirect('alumnos')
        
        # Si la autenticación falla, podrías redirigir a la misma página con un mensaje de error.
        return render(request, 'main.html', {'error': 'Credenciales inválidas'})

    return render(request, 'main.html')

def alumnos(request):
    user_id = request.session.get('user_id')
    if user_id:
        alumnos = Alumno.objects.filter(id=user_id)
        alumno_vigente =Alumno.objects.get(id=user_id)
        return render(request, 'alumnos.html', {'alumnos': alumnos,
                      'alumno_vigente':alumno_vigente})
    else:
        return redirect('main')

def profesores(request):
    user_id = request.session.get('user_id')
    if user_id:
        profesor_vigente = Profesor.objects.get(id=user_id)
        profesores = Profesor.objects.filter(id=user_id)
        return render(request, 'profesores.html', {'profesores': profesores,
                                                   'profesor_vigente': profesor_vigente})
    else:
        return redirect('main')

def grupos(request):
    role = request.session.get('role')
    user_id = request.session.get('user_id')
    if role == 'profesor' and user_id:
        grupos = Grupos.objects.filter(id_profesor_id=user_id)
        profesor_vigente = Profesor.objects.get(id=user_id)
    else:
        return redirect('main')
    
    return render(request, 'grupos.html', {'grupos': grupos,
                                           'profesor_vigente': profesor_vigente})
def profesores_subir(request):
    user_id = request.session.get('user_id')
    if user_id:
        profesor_vigente = Profesor.objects.get(id=user_id)
        
        # Obtener todas las materias relacionadas con los grupos del profesor vigente
        materias_asignadas = Grupos.objects.filter(id_profesor=profesor_vigente).values_list('nombre_mat_id', flat=True)
        
        if request.method == 'POST':
            form = CalificacionForm(request.POST)
            if form.is_valid():
                calificacion = form.save(commit=False)
                calificacion.id_profesor = profesor_vigente
                calificacion.save()
                return redirect('subir')  # Redirige a la misma página después de agregar la calificación
        else:
            form = CalificacionForm()
        
        # Filtrar el formulario para mostrar solo las materias que el profesor puede asignar
        form.fields['id_materia'].queryset = Materia.objects.filter(id__in=materias_asignadas)
        
        return render(request, 'subir.html', {'form': form,
                      'profesor_vigente': profesor_vigente})
    else:
        return redirect('main')
def horarios(request):
    user_id = request.session.get('user_id')
    if user_id:
        horarios = Horario.objects.all()
        alumno_vigente =Alumno.objects.get(id=user_id)
    return render(request, 'horariosA.html', {'horarios': horarios,
                                              'alumno_vigente':alumno_vigente}) 
def cerrar_sesion(request):
    request.session.flush()  # Esto elimina todos los datos de la sesión
    return redirect('main')