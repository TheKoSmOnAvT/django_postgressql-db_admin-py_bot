from django.shortcuts import render
from .forms import UserForm
from django.http import HttpResponse
from .models import Person
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView

import traceback

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def index(request):
    people = Person.objects.all()
    return render(request, "laba1/LABA1.html", locals())

def query(request):
    people = Person.objects.all()
    return render(request, "laba1/query.html")

def bd(request):
    query = request.POST.get("query")


    from django.db import connection, Error
    try:
        with connection.cursor() as cursor:
            cursor.execute(query) #выполняем запрос 
            try:
                desc = cursor.description #берем заголовки 
                try:
                    attrib =[col[0] for col in desc] 
                except:
                    data = {"Errors" : "Magic", 'Query' : query}
                    return render(request, "laba1/query.html", data)
                mas = cursor.fetchall() #берем массив данных (результаты запроса)
                data = {"keys": attrib, "dates": mas, 'Query' : query}
                return render(request, "laba1/query.html", context=data)
            except Error as e:
                data = {"Errors" : str(e), 'Query' : query}
                return render(request, "laba1/query.html", data)
        
    except Error as e:
        data = {"Errors" : str(e), 'Query' : query}
        return render(request, "laba1/query.html", data)