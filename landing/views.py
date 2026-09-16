from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponseNotFound
# Create your views here.
# landing\views.py

stack = ["python", "Django", "Golang", "PHP", "JS"]


def index(request):
    name = "Bryan ochoa"
    return render(request, 'landing/landing.html', {
        "name": name,
        "date": datetime.now(),
        "stack": stack
    })


def tools(request, tool):
    try:
        index = stack.index(tool.upper())
        if not index >= 0:
            return HttpResponseNotFound("No se encontro tu pendejada padrino")
        title = stack[index]
        return render(request, 'landing/stack-details.html', {
            "title": title
        })

    except:
        return HttpResponseNotFound("No se encontro tu pendejada padrino")
