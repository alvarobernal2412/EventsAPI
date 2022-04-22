from django.http import HttpResponse

def primerEjemplo(request): #primera vista
    return HttpResponse("Hola mundo")