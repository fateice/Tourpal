# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection,transaction  
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from hiker.hithiker.models import *  
import MySQLdb

def welcome(request):
    return render_to_response('hithiker/welcome.html')

def index(request):
    if 'signin_email' in request.POST and 'signin_password' in request.POST:
        signin_email = request.POST['signin_email']
        signin_password = request.POST['signin_password']
        response = HttpResponseRedirect('/index/')
        response.set_cookie('useremail',signin_email,3600)
        cursor=connection.cursor()  
        sql='select * from user where email=\''+signin_email+'\' AND password=\''+signin_password+'\''  
        i = cursor.execute(sql)  
        userinfo = cursor.fetchall()
        cursor.close()
        if i != 0:
            response = render_to_response('hithiker/index.html')
            response.set_cookie('useremail',signin_email)
            return response
        else:
            return render_to_response('hithiker/welcome.html')
    elif "useremail" in request.COOKIES:
        return render_to_response('hithiker/index.html')
    else:
        return render_to_response('hithiker/forbid.html')

def destinations(request):
    return render_to_response('hithiker/destinations.html')

def match(request):
    return render_to_response('hithiker/match.html')

def userinfo(request):
    if 'useremail' in request.POST and 'password' in request.POST and 'username' in request.POST:
        username = request.POST['username']
        useremail = request.POST['useremail']
        password = request.POST['password']
        cursor=connection.cursor()  
        sql='insert into user (name,email,password) values (\''+username+'\',\''+useremail+'\',\''+password+'\')'  
        cursor.execute(sql)  
        transaction.commit_unless_managed()  
        cursor.close()  
        dic={'username':username,'email':useremail}
        response = render_to_response('hithiker/userinfo.html',dic)
        response.set_cookie('useremail',useremail)
        return response
    elif 'username' in request.POST and 'age' in request.POST and 'sex' in request.POST and 'phone' in request.POST and 'city' in request.POST and 'hobby' in request.POST:
        username = request.POST['username']
        age = request.POST['age']
        sex = request.POST['sex']
        phone = request.POST['phone']
        city = request.POST['city']
        hobby = request.POST['hobby']
        email =  request.COOKIES['useremail']
        cursor=connection.cursor()
        sql='update user SET name=\''+username+'\' , age=\''+age+'\' , sex=\''+sex+'\' , phone=\''+phone+'\' , city=\''+city+'\' , hobby=\''+hobby+'\' where email=\''+email+'\''  
        cursor.execute(sql)  
        transaction.commit_unless_managed()  
        sql='select * from user where email=\''+email+'\''  
        cursor.execute(sql)  
        user = cursor.fetchall()
        cursor.execute('SELECT userid FROM user WHERE email=\''+email+'\'')
        userid = cursor.fetchall()
        cursor.execute('SELECT groupid,groupname FROM groupinfo WHERE userid=\''+str(userid[0][0])+'\'')
        groupinfo = cursor.fetchall()
        cursor.close()  
        dic={'username':username,'age':age,'sex':sex,'phone':phone,'city':city,'hobby':hobby,'email':email,'groupinfo':groupinfo}
        return render_to_response('hithiker/userprofile.html',dic)
    elif "useremail" in request.COOKIES:
        email = request.COOKIES['useremail']
        cursor=connection.cursor()
        sql='select * from user where email=\''+email+'\''  
        cursor.execute(sql)  
        user = cursor.fetchall()
        cursor.execute('SELECT userid FROM user WHERE email=\''+email+'\'')
        userid = cursor.fetchall()
        cursor.execute('SELECT groupid,groupname FROM groupinfo WHERE userid=\''+str(userid[0][0])+'\'')
        groupinfo = cursor.fetchall()
        dic={}
        for userinfo in user:
            dic={'username':userinfo[1],'age':userinfo[2],'sex':userinfo[3],'phone':userinfo[4],'city':userinfo[5],'hobby':userinfo[6],'email':email,'groupinfo':groupinfo}
        cursor.close()
        return render_to_response('hithiker/userinfo.html',dic)
    else:
        return render_to_response('hithiker/forbid.html')

def userprofile(request):
    if "useremail" in request.COOKIES:
        email = request.COOKIES['useremail']
        cursor=connection.cursor()
        sql='select * from user where email=\''+email+'\''  
        cursor.execute(sql)  
        user = cursor.fetchall()
        cursor.execute('SELECT userid FROM user WHERE email=\''+email+'\'')
        userid = cursor.fetchall()
        cursor.execute('SELECT groupid,groupname FROM groupinfo WHERE userid=\''+str(userid[0][0])+'\'')
        groupinfo = cursor.fetchall()
        dic={}
        for userinfo in user:
            dic={'username':userinfo[1],'age':userinfo[2],'sex':userinfo[3],'phone':userinfo[4],'city':userinfo[5],'hobby':userinfo[6],'email':email,'groupinfo':groupinfo}
        cursor.close()
        return render_to_response('hithiker/userprofile.html',dic)
    else:
        return render_to_response('hithiker/forbid.html')

def groupinfo(request):
    if "useremail" in request.COOKIES:
        if "groupid" in request.GET:
            groupid = request.GET['groupid']
            email = request.COOKIES['useremail']
            cursor = connection.cursor()
            sql = 'SELECT * FROM grouplist WHERE group_id = \''+groupid+'\''
            cursor.execute(sql)
            groupinfo = cursor.fetchall()
            sql = 'SELECT userid FROM user WHERE email=\''+email+'\''
            cursor.execute(sql)
            userid_a = cursor.fetchall()
            userid = str(userid_a[0][0])
            flag = 0
            sql = 'SELECT * FROM groupinfo WHERE groupid=\''+groupid+'\' AND userid=\''+userid+'\''
            if cursor.execute(sql)!=0:
                flag = 1
            cursor.close()
            dic={'groupinfo':groupinfo,'flag':flag}
            return render_to_response('hithiker/groupinfo.html',dic)
        elif "team" in request.GET:
            groupid = request.GET['team']
            cursor = connection.cursor()
            sql='SELECT userid FROM groupinfo WHERE groupid=\''+groupid+'\''
            cursor.execute(sql)
            userid = cursor.fetchall()
            cursor.close()
            return render_to_response('hithiker/groupinfo.html')
        else:
            return render_to_response('hithiker/forbid.html')
    else:
        return render_to_response('hithiker/forbid.html')

def criuses(request):
    if "useremail" in request.COOKIES:
        email = request.COOKIES['useremail']
        return render_to_response('hithiker/criuses.html')
    else:
        return render_to_response('hithiker/forbid.html')

def criuses_result(request):
    if "useremail" in request.COOKIES:
        email = request.COOKIES['useremail']
        groupdate = request.POST['groupdate']
        check_box_list = request.REQUEST.getlist('k')
        radio_list = request.REQUEST.get('number')
        sex_list = request.REQUEST.getlist('sex')
        if len(check_box_list)>0 and len(radio_list)>0 and len(sex_list)>0:
            cursor=connection.cursor()
            full=[]
            ho=[]
            boy = 0
            girk = 0
            #method1, hobby only.
            #for i in range(len(check_box_list)):
            #    sql = 'SELECT * from grouplist where hobby= \''+check_box_list[int(i)]+'\''
            #    cursor.execute(sql)
            #    all=cursor.fetchall()
            #    full.extend(all)

            #method2, hobby, number
            #for i in range(len(check_box_list)):
            #    sql = 'SELECT * from grouplist where hobby= \''+check_box_list[int(i)]+'\''
            #    cursor.execute(sql)
            #    all=cursor.fetchall()
            #    for j in range(len(all)):
            #        num=0
            #        sql = 'SELECT COUNT(*) from groupinfo where groupid=\''+str(all[j][0])+'\'' 
            #        cursor.execute(sql)
            #        num=cursor.fetchall()
            #        num = int(num[0][0])
            #        if int(radio_list)==0:
            #            if num<6:                       
            #                sql = 'UPDATE grouplist SET number=\''+str(num)+'\' where group_id=\''+str(all[j][0])+'\'' 
            #                cursor.execute(sql)
            #                full.append(all[j])
            #        elif int(radio_list)==1:
            #            if num>5 and num<16:                       
            #                sql = 'UPDATE grouplist SET number=\''+str(num)+'\' where group_id=\''+str(all[j][0])+'\'' 
            #                cursor.execute(sql)      
            #                full.append(all[j])                  
            #        elif int(radio_list)==2:
            #            if num>15:                       
            #                sql = 'UPDATE grouplist SET number=\''+str(num)+'\' where group_id=\''+str(all[j][0])+'\'' 
            #                cursor.execute(sql)     
            #                full.append(all[j])                   
            #        else:                             
            #            sql = 'UPDATE grouplist SET number=\''+str(num)+'\' where group_id=\''+str(all[j][0])+'\'' 
            #            cursor.execute(sql)
            #            full.append(all[j])

            #method3, sex, hobby, number
        
            for i in range(len(check_box_list)):
                sql = 'SELECT * from grouplist where hobby= \''+check_box_list[int(i)]+'\' and date = \''+groupdate+'\''
                cursor.execute(sql)
                all=cursor.fetchall()
                for j in range(len(all)):
                    num = 0
                    boy = 0
                    girl = 0
                    sql = 'SELECT COUNT(*) from groupinfo where groupid=\''+str(all[j][0])+'\'' 
                    cursor.execute(sql)
                    num=cursor.fetchall()
                    num = int(num[0][0])

                    sql = 'SELECT * from groupinfo where groupid=\''+str(all[j][0])+'\'' 
                    cursor.execute(sql)
                    temp = cursor.fetchall()
                    for k in range(len(temp)): 
                        sql = 'SELECT * from user where userid=\''+str(temp[k][2])+'\' and sex=\''+'男'+'\' '
                        sql2 = 'SELECT * from user where userid=\''+str(temp[k][2])+'\' and sex=\''+'0'+'\' '
                        if(cursor.execute(sql) or cursor.execute(sql2)):
                            boy += 1
                        sql = 'SELECT * from user where userid=\''+str(temp[k][2])+'\' and sex=\''+'女'+'\' '
                        sql = 'SELECT * from user where userid=\''+str(temp[k][2])+'\' and sex=\''+'1'+'\' '
                        if(cursor.execute(sql) or cursor.execute(sql2)):
                            girl += 1
                    if int(radio_list)==0:
                        if num<6:                       
                            sql = 'UPDATE grouplist SET number=\''+str(num)+'\' where group_id=\''+str(all[j][0])+'\'' 
                            cursor.execute(sql)

                            if len(sex_list)==2:
                                full.append(all[j])
                            elif sex_list[0] == '0':
                                if boy == num:
                                    full.append(all[j])
                            elif sex_list[0] =='1':
                                if girl == num:
                                    full.append(all[j])

                    elif int(radio_list)==1:
                        if num>5 and num<16:                       
                            sql = 'UPDATE grouplist SET number=\''+str(num)+'\' where group_id=\''+str(all[j][0])+'\'' 
                            cursor.execute(sql)    
                          
                            if len(sex_list)==2:
                                full.append(all[j])
                            elif sex_list[0] == '0':
                                if boy==num:
                                    full.append(all[j])
                            elif sex_list[0] =='1':
                                if girl == num:
                                    full.append(all[j])
                                                                                
                    elif int(radio_list)==2:
                        if num>15:                       
                            sql = 'UPDATE grouplist SET number=\''+str(num)+'\' where group_id=\''+str(all[j][0])+'\'' 
                            cursor.execute(sql)     
                            if len(sex_list)==2:
                                full.append(all[j])
                            elif sex_list[0] == '0':
                                if boy==num:
                                    full.append(all[j])
                            elif sex_list[0] =='1':
                                if girl == num:
                                    full.append(all[j])               
                    else:                             
                        sql = 'UPDATE grouplist SET number=\''+str(num)+'\' where group_id=\''+str(all[j][0])+'\'' 
                        cursor.execute(sql)
                        if len(sex_list)==2:
                            full.append(all[j])
                        elif sex_list[0] == '0':
                            if boy==num:
                                full.append(all[j])
                        elif sex_list[0] =='1':
                            if girl == num:
                                full.append(all[j])
            
            transaction.commit_unless_managed()  
            cursor.close()
            return render_to_response('hithiker/criuses_result.html',{'check_box_list':check_box_list,'email':email,'full':full,'sex_list':sex_list,'check_box_list':check_box_list})
        else:
            return render_to_response('hithiker/criuses.html')
    else:
        return render_to_response('hithiker/forbid.html')

def criuses_join(request):
    if "useremail" in request.COOKIES:
        email = request.COOKIES['useremail']
        team_id = request.GET['id']
        cursor=connection.cursor()
        sql = 'SELECT * from user where email= \''+email+'\''
        cursor.execute(sql)
        all = cursor.fetchall()
        sql = 'SELECT name from grouplist where group_id=\''+team_id+'\''
        cursor.execute(sql)
        groupname = cursor.fetchall()
        userid = str(all[0][0])
        already = 0

        sql = 'SELECT * from groupinfo where groupid=\''+team_id+'\' and userid=\''+userid+'\''
        if(cursor.execute(sql)):
            already = 1
        else:
            sql = 'INSERT into groupinfo (groupid,userid,groupname) value (\''+team_id+'\', \''+userid+'\',\''+groupname[0][0]+'\')'
            cursor.execute(sql)
            all = cursor.fetchall()
            transaction.commit_unless_managed()  
            cursor.close() 
        return render_to_response('hithiker/criuses_join.html',{'team_id':team_id,'userid':userid,'already':already})
    else:
        return render_to_response('hithiker/forbid.html')

def group(request):
    if "useremail" in request.COOKIES:
        cursor = connection.cursor()
        sql = 'select name from grouplist order by number desc limit 6'
        cursor.execute(sql)
        team_name = cursor.fetchall()
        team_name1 = team_name[0][0]
        team_name2 = team_name[1][0]
        team_name3 = team_name[2][0]
        team_name4 = team_name[3][0]
        team_name5 = team_name[4][0]
        team_name6 = team_name[5][0]
    # name = {'team_name1':team_name[0][0],'team_name2':team_name[1][0],'team_name3':team_name[2][0],'team_name4':team_name[3][0],'team_name5':team_name[4][0],}
        sql = 'select introduction from grouplist order by number desc limit 6'
        cursor.execute(sql)
        team_info = cursor.fetchall()
        team_info1 = team_info[0][0]
        team_info2 = team_info[1][0]
        team_info3 = team_info[2][0]
        team_info4 = team_info[3][0]
        team_info5 = team_info[4][0]
        team_info6 = team_info[5][0]

        sql = 'select group_id from grouplist order by number desc limit 6'
        cursor.execute(sql)
        team_id = cursor.fetchall()
        team_id1 = team_id[0][0]
        team_id2 = team_id[1][0]
        team_id3 = team_id[2][0]
        team_id4 = team_id[3][0]
        team_id5 = team_id[4][0]
        team_id6 = team_id[5][0]
    # info = {'team_info1':introduction[0][0],'team_info2':introduction[1][0],'team_info3':introduction[2][0],'team_info4':introduction[3][0],'team_info5':introduction[4][0],}
        sql = 'select * from grouplist'
        cursor.execute(sql)
        team_all = cursor.fetchall()
        transaction.commit_unless_managed()
        cursor.close()
        return render_to_response('hithiker/group.html',locals())
    else:
        return render_to_response('hithiker/forbid.html')
    # if info:
    #     # name = info.team_name
    #     # message = info.introduce
    #     # city = info.city
    #     # date = info.date
    #     # location = info.destination
    #     # hobby = select
    #     cursor = connection.cursor()
    #     # sql='insert into user (name,email,password) values (\''+username+'\',\''+useremail+'\',\''+password+'\')'  
    #     sql = 'insert into group (name,message,city,date,location,hobby) values (\''+info['team_name']+'\',\''+info['introduce']+'\',\''+info['city']+'\',\''+info['date']+'\',\''+info['destination']+'\',\''+info['select']+'\')'
        
    #     # cursor.execute(sql)  
    #     cursor.execute(sql)
    #     transaction.commit_unless_managed()
    #     cursor.close()
    #     return render_to_response('hithiker/group.html')
    # else:
    #     return render_to_response('hithiker/group.html')

def creategroup(request):
    if "useremail" in request.COOKIES:
        email = request.COOKIES['useremail']
        if 'team_name' in request.GET and 'city' in request.GET and 'destination' in request.GET:
            name = request.GET['team_name']
            introduction = request.GET['introduce']
            city = request.GET['city']
            date = request.GET['date']
            destination = request.GET['destination']
            hobby = request.GET['select']
            cursor = connection.cursor()
            sql='insert into grouplist (name,introduction,city,date,destination,hobby) values (\''+name+'\',\''+introduction+'\',\''+city+'\',\''+date+'\',\''+destination+'\',\''+hobby+'\')'
            cursor.execute(sql)
            transaction.commit_unless_managed()
            sql = 'select name from grouplist order by date desc limit 6'
            cursor.execute(sql)
            team_name = cursor.fetchall()
            team_name1 = team_name[0][0]
            team_name2 = team_name[1][0]
            team_name3 = team_name[2][0]
            team_name4 = team_name[3][0]
            team_name5 = team_name[4][0]
            team_name6 = team_name[5][0]
            # name = {'team_name1':team_name[0][0],'team_name2':team_name[1][0],'team_name3':team_name[2][0],'team_name4':team_name[3][0],'team_name5':team_name[4][0],}
            sql = 'select introduction from grouplist order by date desc limit 6'
            cursor.execute(sql)
            team_info = cursor.fetchall()
            team_info1 = team_info[0][0]
            team_info2 = team_info[1][0]
            team_info3 = team_info[2][0]
            team_info4 = team_info[3][0]
            team_info5 = team_info[4][0]
            team_info6 = team_info[5][0]
            # info = {'team_info1':introduction[0][0],'team_info2':introduction[1][0],'team_info3':introduction[2][0],'team_info4':introduction[3][0],'team_info5':introduction[4][0],}
            transaction.commit_unless_managed()
            sql='SELECT group_id from grouplist where name = \''+name+'\''
            cursor.execute(sql)
            group_id = cursor.fetchall()
            group_id = str(group_id[0][0])
            sql='SELECT userid from user where email = \''+email+'\''
            cursor.execute(sql)
            userid = cursor.fetchall()
            userid = str(userid[0][0])
            sql='INSERT into groupinfo (groupid,userid,groupname) values (\''+group_id+'\',\''+userid+'\',\''+name+'\')'
            cursor.execute(sql)
            transaction.commit_unless_managed()
            cursor.close()
            return render_to_response('hithiker/group.html',locals())
        else:
            return render_to_response('hithiker/creategroup.html')
    else:
        return render_to_response('hithiker/forbid.html')