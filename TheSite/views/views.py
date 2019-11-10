from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.db import connection, Error
import traceback


def print_views(request):
    select_view= request.POST.get("select_view") 
    data = {}
    q_t = "SELECT table_name FROM INFORMATION_SCHEMA.tables WHERE table_type='VIEW' AND table_schema=ANY(current_schemas(false))"
    try:
        data = { "views" : func_sql(q_t)}      
        if select_view!=None:
            data["names"]=select_view
            q_t_1= "SELECT * FROM "+select_view 
            data["selected_tb"] = func_sql(q_t_1)
            data["attrib"] = fun_at(q_t_1)
            printquer(q_t_1)
    except Error as e:
        data["Errors"] = str(e)
    return render(request, "htmls/change_view.html", data)


def del_views(request):
    select_view= request.GET.get("name")
    q_t = "DROP VIEW "+ select_view
    printquer(q_t) 
    sql_change(q_t)
    return HttpResponseRedirect('/views/')
    

def to_create_view(request):
    data ={}
    algorithm = [' ', 'TEMP', 'RECURSIVE']
    options = [' ', 'LOCAL','CASCADED']
    data['alg'] = algorithm
    data['options'] = options
    return render(request, "htmls/create_view.html",data)

def create_view(request):
    select_alg= request.POST.get("select_alg") 
    select_rep= request.POST.get("select_rep") 
    name= request.POST.get("name") 
    select_query= request.POST.get("select_query") 
    select_options= request.POST.get("select_options") 
    q_t = "CREATE "
    if select_rep =='OK':
        q_t+=" OR REPLACE "
    q_t+= select_alg +" VIEW " +name + " AS " + select_query
    if select_options !='':
        q_t+=" WITH " + select_options + " CHECK OPTION"
    printquer(q_t)
    sql_change(q_t)
    return HttpResponseRedirect('/views/')


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

#####