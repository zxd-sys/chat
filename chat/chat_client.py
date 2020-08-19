"""
chat_客户端
"""
from socket import *
from multiprocessing import Process
import sys

ADDR = ("127.0.0.1", 22227)


# 创建接收消息的函数
def recv_msg(sock):
    while True:
        data, addr = sock.recvfrom(1024 * 10)
        msg = "\n" + data.decode() + "\n>>>"
        print(msg, end="")


# 创建发送消息的函数
def send_msg(sock, name):
    while True:
        try:
            content = input(">>>")
        except KeyboardInterrupt:
            content = "exit"
        if content == "exit":
            msg = "E " + name
            sock.sendto(msg.encode(), ADDR)
            sys.exit("退出聊天室!")
        msg = "C %s %s" % (name, content)
        sock.sendto(msg.encode(), ADDR)


# 创建进入聊天室的函数
def login(sock):
    while True:
        name = input("Name:")
        msg = "L " + name
        sock.sendto(msg.encode(), ADDR)
        data, addr = sock.recvfrom(1024)
        # 约定"OK"为允许进入
        if data == b"OK":
            print("进入聊天室")
            return name
        else:
            print("该用户名已被占用!")


# 创建主函数
def main():
    sock = socket(AF_INET, SOCK_DGRAM)

    # 调用进入聊天室的函数
    name = login(sock)
    p = Process(target=recv_msg, args=(sock,))
    p.daemon = True
    p.start()
    send_msg(sock, name)


if __name__ == '__main__':
    main()
