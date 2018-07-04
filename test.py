#!_*_coding: utf-8 _*_
# @author =  lijun
# date  =  2018/7/3/003 20:49

#服务器
#import socketserver

import socket

#1.创建一个socket
#参数1：指定协议 AE_INET 或 AF_INET6
#参数2：SOCK_STREAM执行使用面向流的TCP协议
#sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#2.建立连接
#参数是一个元祖，第一个参数为要连接服务器的ip地址，第二个参数为端口
#sk.connect(('www.sina.com', 80))

#sk.send(b)


childtypenames = '全部分类：0#进口水果：110#国产水果：120'
childtypename_list = childtypenames.split('#')
child_type_name_list = []
for childtypename in childtypename_list:
    child_type_name_list.append(childtypename.split('：'))

print(child_type_name_list)





