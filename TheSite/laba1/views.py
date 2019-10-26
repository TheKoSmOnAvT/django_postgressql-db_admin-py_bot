from django.shortcuts import render
from .forms import UserForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.db import connection, Error
import traceback


def query(request):
    return render(request, "laba1/query.html")

def bd(request):
    query = ""
    query = request.POST.get("query") 
    
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



def func_sql(query):
    try:
        with connection.cursor() as cursor: #получаем список таблиц
            cursor.execute(query)
            try:
                mas = cursor.fetchall() #берем массив данных (результаты запроса)
            except Error as e:
                mas = str(e)
    except Error as e:
       mas = str(e)
    return mas

def fun_at(query):
    try:
        with connection.cursor() as cursor: #получаем список таблиц
            cursor.execute(query)
            try:
                desc = cursor.description #берем заголовки 
                mas = [col[0] for col in desc]  #берем массив данных (результаты запроса)
            except Error as e:
                mas = str(e)
    except Error as e:
       mas = str(e)
    return mas


def table_frombd(request): #функция для отображения списка таблиц в бд
    select_tab = request.POST.get("select_table") 
    data = {}
    q_t = "SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema','pg_catalog');"
    try:
        data = { "tables" : func_sql(q_t)}      
        if select_tab!=None:
            sq = "select * from " + select_tab
            data["selected_tb"] = func_sql(sq)
            data["attrib"] = fun_at(sq)
    except Error as e:
        data["Errors"] = str(e)
    return render(request, "laba1/change_db.html", data)



def change_data(request):
    mas = request.GET.getlist("name")
    print(mas[0][0])
    data = {"datas":mas}
    return render(request, "laba1/change_data.html", data)
