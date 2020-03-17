#coding=utf-8
import pymysql
import json
import subprocess
import os

conn = pymysql.connect("10.126.11.149", "root", "123456", "slb_db")


def remove_load_old_file(filename):
    print(filename)
    stats = 1
    flag = os.path.exists(filename)
    if flag:
        stats = os.remove(filename)
        if stats == 0:
            print("删除老的文件{}成功".format(filename))
    else:
        print("不需要清理")
    return stats


def mvn_package(path,cmd):
    os.chdir(path)
    status = os.system(cmd)
    if status == 0:
        print("Maven编译成功")
    #return status


def getupdate(path):
    os.chdir(path)
    status = os.system("git pull")
    if status == 0:
        print("拉取代码成功")
    return status


def remove_remote_file(host,product_path,filename):
    print("删除老文件:{}".format(product_path+"/"+filename))
    cmd = "ssh "+ host +" rm -rf "+product_path+"/"+filename
    print(cmd)
    status = os.system(cmd)
    if status == 0:
        print("删除文件{}成功".format(product_path+"/"+filename))
    return status


def sync_remote_file(host,project_path,product_path,filename,rename):
    local_file = project_path+"/target/"+filename
    print("发布的文件:{}".format(local_file))
    cmd= "scp -r "+local_file+" "+host+":"+product_path+"/"+rename
    status = os.system(cmd)
    if status == 0:
        print("部署主机{}的文件{}成功".format(host,rename))
    return status


def sync_remote_script(host):
    local_file = "/root/pub.services/kill.sh"
    print("发布的文件:{}".format(local_file))
    cmd= "scp -r "+local_file+" "+host+":"+"/root/"
    print(cmd)
    status = os.system(cmd)
    if status == 0:
        print("部署主机{}的文件{}成功".format(host,"/root/kill.sh"))
    cmd= "ssh "+host+" "+"chmod 755 /root/kill.sh"
    status = os.system(cmd)
    return status


def restart_tomcat(host):
    shutdown_cmd = "ssh "+ host +" /root/kill.sh"
    print(shutdown_cmd)
    startup_cmd = "ssh "+ host +" /usr/local/tomcat/bin/startup.sh"
    status = os.system(shutdown_cmd)
    status = os.system(shutdown_cmd)
    status = os.system(shutdown_cmd)
    status = os.system(shutdown_cmd)    
    
    if status == 0: 
        print("停止Tomcat成功")
    else:
        print("再次停止Tomcat")
        status = os.system(shutdown_cmd)
    print(startup_cmd)
    status = os.system(startup_cmd)
    status = os.system(startup_cmd)
    status = os.system(startup_cmd)
    status = os.system(startup_cmd)
    if status == 0: 
        print("启动Tomcat成功")
    else:
        print("再次启动Tomcat")
        status = os.system(startup_cmd)


def compile(projectname):
    cursor = conn.cursor()
    sql = "select * from project where id='%s'"%(projectname)
    cursor.execute(sql)
    values = cursor.fetchone()
    project_path = values[3]
    project_type = values[4]
    product_path = values[5]
    filename = values[6]
    maven_cmd = values[7]
    rename = values[8]
    print("清理老的编译包文件")
    remove_load_old_file(project_path+"/target/"+filename)
    print("开始拉取新代码")
    getupdate(project_path)
    print("开始执行Maven编译")
    mvn_package(project_path,maven_cmd)
    return "OK"


def publish(projectname):
    cursor = conn.cursor()
    sql = "select * from project where id='%s'"%(projectname)
    cursor.execute(sql)
    values = cursor.fetchone()
    project_path = values[3]
    project_type = values[4]
    product_path = values[5]
    filename = values[6]
    maven_cmd = values[7]
    rename = values[8]
    project_name = values[1]
    print("开始部署项目{}".format(project_name))
    sql = "select * from hosts where project_id='%s'"%(projectname)
    cursor.execute(sql)
    values = cursor.fetchall()
    for host in values:
        print("  正在部署主机:{}".format(host[2]))
        remove_remote_file(host[2],product_path,"*")
        #sync_remote_script(host[2])
        sync_remote_file(host[2],project_path,product_path,filename,rename)
    return "{} publish OK!".format(project_name)

