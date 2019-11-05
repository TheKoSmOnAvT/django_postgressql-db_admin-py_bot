from django.shortcuts import render
#from .forms import UserForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.db import connection, Error
import traceback

def del_trig(request):

    create_trig_html(request)

def off_trig(request):

    create_trig_html(request)

def on_trig(request):

    create_trig_html(request)

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
    create_trig_html(request)


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



#########


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


def check_none(mas):
    for i in range(0,len(mas)):
        for j in range(0,len(mas[i])):
            if mas[i][j] == "None":
                mas[i][j] = "#empty#"
    return mas


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
    check_none(new_data)
    data = {"fields":fields,  "name_table" : name_table,  "new_data":new_data}
    return render(request, "laba1/change_data.html", data)

def chaeck_null(mas, i):
    print(str(mas[i]) )
    if str(mas[i]) == "None" or str(mas[i]) == "#empty#":
        return False
    return True

def set_null(mas, i):
    print(str(mas[i]) )
    if str(mas[i]) == "#empty#":
        return False
    return True

def new_data(request):
    new_data = request.POST.getlist("changes") #методом пост поулчаем новые значения из input
    old_data =  request.GET.getlist("new") #методом гет получаем название таблицы из старые данные в одном массиве 

    old_data = old_data[0].split()
    name = old_data[0] #название таблицы
    old_data = old_data[1:] #старые данные
    
    mas = fun_at("select * from "+name) #получение атрибутов (их названия)
    query ="UPDATE "+name+" SET "
    for i in range(0,len(mas)):
        if set_null(new_data, i):
            query +=" "+ mas[i]+"='"+new_data[i] +"'" 
            if i !=len(mas)-1:
                query +=" ,"
    if query[len(query)-1]==',':
        query = query[0:len(query)-1]
    query+=" WHERE "

    for i in range(0,len(old_data)):
        if chaeck_null(old_data,i):
            query += " "+ mas[i]+"='"+old_data[i]+"'" 
            if i !=len(old_data)-1:
                query +=" and"
    if query[len(query)-1]=='d':
        query = query[0:len(query)-3]
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


def add_column(request):
    mas = request.GET.getlist("name")
    mas = mas[0].split()
    name_table = mas[0] #название таблицы
    mas_at =  fun_at("select * from "+name_table)
    data = {"name_table": name_table,"mas_at":mas_at}
    return  render(request, "laba1/create_attrib.html", data)

def add_column_query(request):
    mas = request.GET.getlist("name")
    mas = mas[0].split()
    name_table = mas[0] #название таблицы
    new_data = request.POST.getlist("changes") #методом пост поулчаем новые значения из input
    query="ALTER TABLE "+name_table+" ADD "+ new_data[0] + ' '+ new_data[1]
    printquer(query)
    sql_change(query)
    return table_frombd(request)


def del_atrib(request):
    mas = request.GET.getlist("name")
    mas = mas[0].split()
    name_table = mas[0] #название таблицы
    name_atrib = mas[1] #название атрибута
    query="ALTER TABLE " + name_table +" DROP COLUMN "+ name_atrib
    printquer(query)
    sql_change(query)
    return table_frombd(request)

def to_change_attrib(request):
    mas = request.GET.getlist("name")
    mas = mas[0].split()
    name_table = mas[0] #название таблицы
    name_atrib = mas[1] #название атрибута
    type_attrib = str(func_sql("SELECT pg_typeof( "+ name_atrib +" ) from "+ name_table +";"))
    type_attrib = type_attrib.replace("(", "")
    type_attrib = type_attrib.replace(")", "")
    type_attrib = type_attrib.replace(",", "")
    type_attrib = type_attrib.replace("'", "")
    type_attrib = type_attrib.replace("[", "")
    type_attrib = type_attrib.replace("]", "")
    printquer(type_attrib)
    data = {"name_table":name_table,"name_atrib":name_atrib,"type_attrib":type_attrib}
    return render(request, "laba1/change_attrib.html", data)

def change_attrib(request):
    mas = request.GET.getlist("name")
    mas = mas[0].split()
    name_table = mas[0] #название таблицы
    old_name_atrib = mas[1] #название атрибута
    new_data = request.POST.getlist("changes") #методом пост поулчаем новые значения из input
    new_name_atrib = new_data[0]
    new_type_atrib = new_data[1]
    query_name="ALTER TABLE "+ name_table + " RENAME "+ old_name_atrib +" TO "+new_name_atrib
    query_type="ALTER TABLE "+ name_table + " ALTER COLUMN "+ old_name_atrib +" TYPE "+ new_type_atrib
    printquer(query_name)
    printquer(query_type)
    sql_change(query_type)
    sql_change(query_name)
    return table_frombd(request)

def to_rename_table(request):
    mas = request.GET.getlist("name")
    mas = mas[0].split()
    name_table = mas[0] #название таблицы
    data = {"name_table":name_table}
    return render(request, "laba1/rename_table.html", data)

def rename_table(request):
    mas = request.GET.getlist("name")
    mas = mas[0].split()
    old_name_table = mas[0] #название таблицы
    new_data = request.POST.getlist("changes") #методом пост поулчаем новые значения из input
    new_name_table = new_data[0]
    query = "ALTER TABLE "+ old_name_table +" RENAME TO "+new_name_table
    printquer(query)
    sql_change(query)
    return table_frombd(request)


def crt_html(request):
    return render(request, "laba1/create_table.html")

def st(mas):
    if len(mas[0])<1 or len(mas[1])<1 :
        return False
    return True


def create_table(request):
    new_data1 = request.POST.getlist("changes1") #методом пост поулчаем новые значения из input
    new_data2 = request.POST.getlist("changes2")
    new_data3 = request.POST.getlist("changes3")
    new_data4 = request.POST.getlist("changes4")
    name_table = request.POST.getlist("name")
    printquer(new_data)
    printquer(name_table)
    query = "CREATE TABLE "+ name_table[0] +" ( "
    if st(new_data1) :
        query+= " "+ new_data1[0]+ " " +new_data1[1] +","
    if st(new_data2) :
        query+= " "+ new_data2[0]+ " " +new_data2[1] +","
    if st(new_data3) :
        query+= " "+ new_data3[0]+ " " +new_data3[1] +","
    if st(new_data4) :
        query+= " "+ new_data4[0]+ " " +new_data4[1] +","
    if query[len(query)-1]==",":
        query=query[0:len(query)-1]
    
    query+= ")"
    printquer(query)
    sql_change(query)
    return table_frombd(request)