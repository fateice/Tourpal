from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection,transaction  
from django.shortcuts import render_to_response,RequestContext
from django.views.decorators.csrf import csrf_protect
from hiker.hithiker.models import *  
import MySQLdb
  
def ClassroonAdd(request):  
    if 'name' in request.GET and request.GET['name'] and 'tutor' in request.GET and request.GET['tutor']:  
        name = request.GET['name']  
        tutor = request.GET['tutor']  
        cursor=connection.cursor()  
        sql='insert into Author (AuthorID,Country,Name,Age) values (\''+name+'\',\''+tutor+'\',\'a\',20)'  
        cursor.execute(sql)  
        transaction.commit_unless_managed()  
        cursor.close()  
          
        return render_to_response('hithiker/Classroom_Add_results.html',  
            {'name': name})  
    else:  
        return render_to_response('hithiker/Classroom_Add.html', {'error': True}) 

def welcome(request):
    return render_to_response('hithiker/welcome.html')

@csrf_protect
def index(request):
    return render_to_response('hithiker/index.html',context_instance=RequestContext(request))
