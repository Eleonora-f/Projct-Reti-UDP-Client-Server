# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 09:06:20 2022

@author: 39345
"""

import socket as sk
import os

BUFFERSIZE = 4096
CLIENT_FOLDER = "client_folder"
server_address = ('localhost', 10000)

menu_message = '\r\nUDP Client-Server Architecture\r\n\r\n' \
                  'Choose an operation:\r\n\r\n' \
                  '- list:\tRequest the list of available file names\r\n' \
                  '- get:\tGet a file from the server\r\n' \
                  '- put:\tUpload a file on the server\r\n' \
                  '- help:\tList of operations\r\n' \
                  '- exit:\tEnd the client process\r\n'
#list function return the files list
def list(sock_client, server_address, option):
    print('\nList of files: \n')
    sock_client.sendto(option.encode(), server_address)
    filedata = int(sock_client.recvfrom(BUFFERSIZE)[0].decode()) 
    if filedata==0:
        print('Error: Empty list')
        return
    for i in range(filedata):
        data, address = sock_client.recvfrom(BUFFERSIZE)
        print(data.decode())
        return
         
#get function download files from server         
def get(sock_client, server_address, option):
    print('\n Getting a file \n')
    sock_client.sendto(option.encode(), server_address)
    file = option.split()[1]
    filepath = os.path.join(CLIENT_FOLDER, file)
    if (os.path.exists(filepath)):
         print("Error: file already downloaded on the directory")
         return
    if not os.path.isdir(CLIENT_FOLDER):
            os.mkdir(CLIENT_FOLDER)
    data, address = sock_client.recvfrom(BUFFERSIZE)
    file_ispresent = data.decode()
    if (file_ispresent == 'OK'):
             with open(filepath,'wb') as file_op:
                  while True:
                     data = sock_client.recvfrom(BUFFERSIZE)[0]
                     if data == b'':
                         break
                     file_op.write(data)
                  file_op.close()
             print('\nFinished Download \n')
    elif (file_ispresent == 'no'):
        print('\n File not valid ...\n')
   
#put function upload files on server's folder  
def put(sock_client, server_address, option):
    print('\n Uploading a file ...\n')
    file = option.split()[1]
    filepath = os.path.join(CLIENT_FOLDER, file)
    if (not os.path.exists(filepath)):
            print('\nError: not existing file\n')
            return
    else:
            sock_client.sendto(option.encode(), server_address)
            with open(filepath,'rb') as file_op:
                while True:
                    data = file_op.read(BUFFERSIZE)
                    if not data:
                        sock_client.sendto(b'', server_address)
                        break
                    sock_client.sendto(data, server_address)
                file_op.close()
            print('\nFinished operation\n')
    
#Main function
if __name__ == '__main__':
    # Start the client and create socket UDP
    sock_client = sk.socket(sk.AF_INET, sk.SOCK_DGRAM) 
    print(menu_message)
    #While loop manages the client's options
    while True:
        option = input('\nEnter your choice: ')
        if option =='list':
             list(sock_client, server_address, option)
             
        elif option.startswith('get'):
             get(sock_client, server_address, option)
             
        elif option.startswith('put'):
             put(sock_client, server_address, option)
              
        elif option == 'help':
             print(menu_message)
             
        elif option == 'exit':
            sock_client.sendto(option.encode(), server_address)
            sock_client.close()
            print('\nClosing...')
            print('\nBye bye :)')
            break
                