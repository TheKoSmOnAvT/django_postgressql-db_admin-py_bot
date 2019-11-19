from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.db import connection, Error
import traceback


# Create your views here.

#select * from information_schema.parameters WHERE specific_schema NOT IN ('information_schema','pg_catalog');

#SELECT * FROM information_schema.routines WHERE specific_schema NOT IN ('information_schema','pg_catalog');
#SELECT routine_name FROM information_schema.routines WHERE specific_schema NOT IN ('information_schema','pg_catalog');
    

def create_func(request):
    select_rep= request.POST.get("select_rep")
    name= request.POST.get("name")
    arg= request.POST.get("arg")
    type= request.POST.get("type")
    query= request.POST.get("query")
    p=''
    if select_rep=="OK":
        p="OR REPLACE "
    q_t = "CREATE " + p + "FUNCTION "+ name +"( "+ arg +" ) RETURNS " + type +" AS $$ "+ query + " $$  LANGUAGE SQL;"
    printquer(q_t)
    sql_change(q_t)
    return HttpResponseRedirect('/func/')


def to_create_html(request):
    return render(request, "create_function.html")

def del_func(request):
    mas = request.GET.getlist("name")
    name = mas[0]
    q_t="DROP FUNCTION "+name 
    try:
        sql_change(q_t)
    except Error as e:
        data["Errors"] = str(e)
    printquer(q_t)
    return HttpResponseRedirect('/func/')


def to_func(request):
    q_t = "SELECT routine_name FROM information_schema.routines WHERE specific_schema NOT IN ('information_schema','pg_catalog');"
    data={}
    try:
        func = func_sql(q_t)
        data['func']=func
        select_func= request.POST.get("select_func")
        if select_func!=None:
            q_t1="SELECT * FROM information_schema.routines WHERE specific_schema NOT IN ('information_schema','pg_catalog') and routine_name = '"+ select_func+"'"
            q_t2="SELECT routine_definition FROM information_schema.routines WHERE specific_schema NOT IN ('information_schema','pg_catalog') and routine_name = '"+ select_func+"'"
            data['names']=select_func
            data["attrib"] = fun_at(q_t1)
            data["selected_func"] = func_sql(q_t1)
            data["code"] = func_sql(q_t2)
    except Error as e:
        data["Errors"] = str(e)
    return render(request,"change_functions.html",data)



def convrt(type_attrib):
    type_attrib = type_attrib.replace("(", "")
    type_attrib = type_attrib.replace(")", "")
    type_attrib = type_attrib.replace(",", "")
    type_attrib = type_attrib.replace("'", "")
    type_attrib = type_attrib.replace("[", "")
    type_attrib = type_attrib.replace("]", "")
    return type_attrib


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


def printquer(query): ##принт в консоль
    print("##query##")
    print(query)
    print("#######")

def sql_change(query): #без возврата данных
    try:
        with connection.cursor() as cursor: #sql 
            cursor.execute(query)     
    except Error as e:
       print(str(e))


def fun_at(query): #attribs
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
#########
