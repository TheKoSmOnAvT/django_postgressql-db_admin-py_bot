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

def sql_change(query): #без возврата данных
    try:
        with connection.cursor() as cursor: #sql 
            cursor.execute(query)     
    except Error as e:
       print(str(e))

def table_frombd(request): #функция для отображения списка таблиц в бд и саму бд
    select_tab = request.POST.get("select_table") 
    data = {}
    q_t = "SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema','pg_catalog');"
    try:
        data = { "tables" : func_sql(q_t)}      
        if select_tab!=None:
            sq = "select * from " + select_tab
            data["selected_tb"] = func_sql(sq)
            data["attrib"] = fun_at(sq)
            data["name_table"] = select_tab
    except Error as e:
        data["Errors"] = str(e)
    return render(request, "laba1/change_db.html", data)



def change_data(request): #функция изменения выборки
    mas = request.GET.getlist("name")
    mas = mas[0].split()
    name_table = mas[0]
    fields = mas[1:]
    mas_atrib = fun_at("select * from "+name_table)

    new_data=[]
    for i in range(0,len(mas_atrib)) :
            new_data.append([mas_atrib[i], None])
    for i in range(0,len(fields)) :
            new_data[i][1]= fields[i]

    data = {"fields":fields,  "name_table" : name_table,  "new_data":new_data}
    return render(request, "laba1/change_data.html", data)

def new_data(request):
    new_data = request.POST.getlist("changes") #методом пост поулчаем новые значения из input
    old_data =  request.GET.getlist("new") #методом гет получаем название таблицы из старые данные в одном массиве 

    old_data = old_data[0].split()
    name = old_data[0] #название таблицы
    old_data = old_data[1:] #старые данные
    
    mas = fun_at("select * from "+name) #получение атрибутов (их названия)
    query ="UPDATE "+name+" SET "
    for i in range(0,len(mas)):
        query += mas[i]+"='"+new_data[i] +"'" 
        if i !=len(mas)-1:
            query +=" , "
    query+=" WHERE "
    for i in range(0,len(old_data)):
        query += mas[i]+"='"+old_data[i]+"'" 
        if i !=len(old_data)-1:
            query +=" and "
    printquer(query)
    sql_change(query)
    return table_frombd(request)

def del_data(request):
    mas = request.GET.getlist("name")
    mas = mas[0].split()
    name_table = mas[0] #название таблицы
    fields = mas[1:] #старые данные
    mas_atrib = fun_at("select * from "+name_table) #получение атрибутов (их названия)
    query="DELETE FROM "+name_table+" WHERE "
    for i in range(0,len(fields)):
        query += mas_atrib[i]+"='"+fields[i]+"'" 
        if i !=len(fields)-1:
            query +=" and "
    printquer(query)
    sql_change(query) #sql
    return table_frombd(request)

def add_data_name(request): #заполнение формы под добавление данных
    mas = request.GET.getlist("name")
    mas = mas[0].split()
    name_table = mas[0] #название таблицы
    mas_atrib = fun_at("select * from "+name_table) 
    data = {"name_table" : name_table, "mas_atrib" : mas_atrib}
    return render(request, "laba1/add_data.html", data)

def add_data(request): #выполнение добавления 
    new_data = request.POST.getlist("changes") #методом пост поулчаем новые значения из input
    
    mas = request.GET.getlist("name")
    mas = mas[0].split()
    name_table = mas[0] #название таблицы
    query = "INSERT INTO "+name_table+" VALUES ( "

    for i in range(0,len(new_data)):
        query +=" '"+new_data[i]+"' " 
        if i !=len(new_data)-1:
            query +=" , "
    query +=")"
    printquer(query)
    sql_change(query) #sql
    return table_frombd(request)

def truncate_table(request):
    mas = request.GET.getlist("name")
    mas = mas[0].split()
    name_table = mas[0] #название таблицы
    query="TRUNCATE TABLE " + name_table
    printquer(query)
    sql_change(query)
    return table_frombd(request)

def delete_table(request):
    mas = request.GET.getlist("name")
    mas = mas[0].split()
    name_table = mas[0] #название таблицы
    query = "DROP TABLE "+ name_table
    printquer(query)
    sql_change(query)
    return table_frombd(request)

def printquer(query): ##принт в консоль
    print("##query##")
    print(query)
    print("#######")