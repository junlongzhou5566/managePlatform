#!/usr/bin/env python
# coding=utf-8
import os
import pymysql


def get_service():
    conn = pymysql.connect("10.126.11.149", "root", "123456", "slb_db")
    cursor = conn.cursor()
    sql = "select * from service_monitor"
    cursor.execute(sql)
    os.system('cd /home/node_health')
    with open('test.txt', 'w+') as f:
        for i in cursor.fetchall():
            print(i[4])
            if i[4] == '0':
                print(i[1], i[4])
            content = i[1]+'|'+i[2]+'|'+i[3]+'\n'
            f.write(content)
    f.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    get_service()
