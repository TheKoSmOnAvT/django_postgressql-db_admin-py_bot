from django.shortcuts import render
#from .forms import UserForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.db import connection, Error
import traceback



def create_trig_html(request):
    q_t = "SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema','pg_catalog');"
    try:
        data = { "tables" : func_sql(q_t)}      
    except Error as e:
        data["Errors"] = str(e)
    data["times"] = ["BEFORE","AFTER"]
    data["event"] = ["INSERT","UPDATE", "DELETE"]
    funcs_qt ="SELECT routine_name FROM information_schema.routines WHERE routine_type='FUNCTION' AND specific_schema='public';"
    funcs = func_sql(funcs_qt)
    data["funcs"] = funcs
    return render(request, "htmls/create_triger.html", data)

def create_trig_in_bd(request):
    select_table = request.POST.get("select_table") 
    name = request.POST.get("name") 
    select_time = request.POST.get("select_time") 
    select_event = request.POST.get("select_event") 
    select_funcs = request.POST.get("select_funcs") 
    sql_opr = request.POST.get("sql_opr")
    q_t = "CREATE TRIGGER "+ name +" "+select_time + " " + select_event + " ON " + select_table + " FOR EACH ROW EXECUTE PROCEDURE  " + select_funcs + " ();"
    printquer(q_t)
    sql_change(q_t)
    return HttpResponseRedirect('/triger/')


def print_trigers(request):
    select_triger= request.POST.get("select_triger") 
    data = {}
    q_t = "SELECT trigger_name FROM information_schema.triggers"
    try:
        data = { "trigers" : func_sql(q_t)}      
        if select_triger!=None:
            data["names"]=select_triger
            q_t_1= "SELECT * FROM information_schema.triggers where trigger_name like '"+select_triger + "' "
            data["selected_tb"] = func_sql(q_t_1)
            data["attrib"] = fun_at(q_t_1)
            printquer(q_t_1)
    except Error as e:
        data["Errors"] = str(e)
    return render(request, "htmls/change_trigers.html", data)


def del_trig(request):
    mas = request.GET.getlist("name")
    name = mas[0] #имя тригера 
    q_t_1= "SELECT event_object_table FROM information_schema.triggers where trigger_name like '"+name + "' "#	event_object_table
    name_table = func_sql(q_t_1)
    name_table = convrt(str(name_table)) #имя таблицы   
    q_t = "DROP TRIGGER "+name + " ON "+ name_table
    printquer(q_t)
    sql_change(q_t)
    return HttpResponseRedirect('/triger/')

def off_trig(request):
    mas = request.GET.getlist("name")
    name = mas[0] #имя тригера 
    q_t_1= "SELECT event_object_table FROM information_schema.triggers where trigger_name like '"+name + "' "#	event_object_table
    name_table = func_sql(q_t_1)
    name_table = convrt(str(name_table)) #имя таблицы   
    q_t = "ALTER TABLE " + name_table + " DISABLE TRIGGER " + name
    printquer(q_t)
    sql_change(q_t)
    return HttpResponseRedirect('/triger/')


def on_trig(request):
    mas = request.GET.getlist("name")
    name = mas[0] #имя тригера 
    q_t_1= "SELECT event_object_table FROM information_schema.triggers where trigger_name like '"+name + "' "#	event_object_table
    name_table = func_sql(q_t_1)
    name_table = convrt(str(name_table)) #имя таблицы   
    q_t = "ALTER TABLE " + name_table + " ENABLE TRIGGER " + name
    printquer(q_t)
    sql_change(q_t)
    return HttpResponseRedirect('/triger/')


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

