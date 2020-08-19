"""
author: zxd
email:2115296503@qq.com
time: 2020-8-14
env: python 3.6
Process and socket
"""
from socket import *
from multiprocessing import Process

# 创建地址
HOST = "0.0.0.0"
PORT = 22227
ADDR = (HOST, PORT)

# 创建用户字典用来储存所有进入聊天室的用户
user = {}


# 将转发消息封装为函数
def chat(sock, name, content):
    msg = "%s:%s" % (name, content)
    for i in user:
        if i == name:
            continue
        else:
            sock.sendto(msg.encode(), user[i])


# 创建退出函数
def exit01(sock, name):
    del user[name]
    msg = "%s退出聊天室!" % name
    for i in user:
        sock.sendto(msg.encode(), user[i])


# 创建判断用户是否重复的函数
def login(sock, name, addr):
    if name in user or "管理" in name:
        msg = "FAIL"
        sock.sendto(msg.encode(), addr)
        return  # 如果用户存在,结束函数
    else:
        sock.sendto(b"OK", addr)  # 通知用户进入聊天室
        msg = "欢迎%s进入聊天室" % name
        for i in user:
            sock.sendto(msg.encode(), user[i])
        user[name] = addr


# 创建子进程
def request(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        # 解析收到的消息
        tmp = data.decode().split(" ", 2)
        # 判断收到的消息,决定该调用何种函数
        if tmp[0] == "L":
            login(sock, tmp[1], addr)
        elif tmp[0] == "C":
            chat(sock, tmp[1], tmp[2])
        elif tmp[0] == "E":
            exit01(sock, tmp[1])


# 创建主进程
def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(ADDR)

    # 创建进程
    p = Process(target=request, args=(sock,))
    p.daemon = True
    p.start()
    # p.join()
    while True:
        content = input("管理员消息:")
        if content == "exit":
            break
        msg = "C 管理员 " + content
        # 从父进程给子进程发送消息
        sock.sendto(msg.encode(), ADDR)


if __name__ == '__main__':
    main()
