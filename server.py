# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 08:54:56 2022

@author: 39345
"""
import os
import socket as sk
import threading

BUFFERSIZE = 4096
SERVER_FOLDER = 'server_folder' 
server_address = ('localhost', 10000)

#list function send the files list
def list(sock_server, client_address, option):
    if not os.path.isdir(SERVER_FOLDER):
       os.mkdir(SERVER_FOLDER)
    files = os.listdir(SERVER_FOLDER)
    len_file = len(files)
    sock_server.sendto(str(len_file).encode(), client_address)
    data = "\n".join(f for f in files)
    sock_server.sendto(data.encode(), client_address) 
    print('\nShowing list...\n')

#send function send the file requested by the client
def send(sock_server, client_address, option):
    print('\nSending a file...\n')
    file = option.split()[1]
    filepath = os.path.join(SERVER_FOLDER, file)
    if (os.path.exists(filepath)):
        sock_server.sendto('OK'.encode(), client_address)
        with open(filepath,'rb') as file_op:
            data = file_op.read(BUFFERSIZE)
            while data != b'':
                sock_server.sendto(data, client_address)
                data = file_op.read(BUFFERSIZE)
            sock_server.sendto(b'', client_address)
            file_op.close()
        print('\nFinished operation\n')
    else:
         print('\nFile doesn\'t exist\n')
         sock_server.sendto('no'.encode(), client_address)
   
#receive function upload the file          
def receive(sock_server, client_address, option):
    print('\nReceiving a file ...\n')
    if not os.path.isdir(SERVER_FOLDER):
            os.mkdir(SERVER_FOLDER)
    file = option.split()[1]
    filepath = os.path.join(SERVER_FOLDER, file)
    if (os.path.exists(filepath)):
        print('\nError: file already exists')
        return
    else:
        with open(filepath,'wb') as file_op:
            while True:
                data, address = sock_server.recvfrom(BUFFERSIZE)
                if data == b'':
                    break
                file_op.write(data)
            file_op.close()
        print('\nFinished operation\n')

#client_handler function manages the client's options
def client_handler(option, client_address, sock_server):
    if option == 'list':
        list(sock_server, client_address, option)
    elif option.startswith('get'):
        send(sock_server, client_address, option)
    elif option.startswith('put'):
        receive(sock_server, client_address, option)
    elif option == 'exit':
        sock_server.close()
        print('\nClosing...')
        print('\nBye bye :)')
        exit()
        
#Main function      
if __name__ == '__main__':
    print('\n Server is starting...\n')
    # Start the server and create socket UDP
    sock_server = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    sock_server.bind(server_address)
    #While loop manages client's requests 
    #Each time a new request occurs a new thread is created 
    while True:
        print('\n Server is listening...\n')
        data, client_address = sock_server.recvfrom(BUFFERSIZE)
        option = data.decode('utf8')
        
        thread = threading.Thread(target=client_handler, args=(option, client_address, sock_server))
        thread.start()
        thread.join()
        