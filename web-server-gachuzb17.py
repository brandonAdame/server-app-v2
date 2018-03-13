# assn2 Mini Server program written by: Brandon Gachuz (gachuzb17)
# Using python version: 3.6.3
# Tested using Firefox internet browser

import socket


# import os
# import sys

def to_download_link():
    """This function produces the download link to the client"""
    with open('link.html', 'r') as linkFile:
        l_data = linkFile.read()
        c_len = str(len(l_data))

        hdr = "HTTP/1.0 200 OK\r\nContent-Length:" + c_len + "\r\n\n"
        print("Client requested download link")
        client_socket.send((hdr + l_data).encode())
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()


def to_info_page():
    """This function produces the info page to the client"""
    with open('info.html', 'r') as infoFile:
        f_data = infoFile.read().replace('\n', '')
        cnt_len = str(len(f_data))
        head = "HTTP/1.0 200 OK\r\nContent-Length:" + cnt_len + "\r\n\n"
        print("Client requested info page")
        client_socket.send((head + f_data).encode())
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()


def produce_page1():
    """This function will display page1.html to the web browser"""
    # read html file in
    with open('page1.html', 'r') as myfile:
        file_data = myfile.read().replace('\n', '')
        # obtain length of data to be sent
        content_len = str(len(file_data))
        # prepare HTML header
        header = "HTTP/1.0 200 OK\r\nContent-Length:" + content_len + \
                 "\r\n\n"
        print("Client requested page1")
        client_socket.send((header + file_data).encode())  # Sends HTML data
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()


def distribute_download():
    """Distribute download will send the zip file contained in this project's
    directory to the web browser"""
    with open('download.zip', 'rb') as zip_file:
        z_data = zip_file.read()
        c_len = str(len(z_data))
        hd = "HTTP/1.0 200 OK\r\nContent-Length:" + c_len + \
             "\r\nContent-Type: application/zip" \
             "\r\nContent Disposition: " \
             "attachment;filename=\"download.zip\"\r\n\n"
        print("Client requested download.zip")
        client_socket.send(hd.encode())
        client_socket.send(z_data)
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()


def send_echo():
    """Send echo will echo the message 'Echoing' to the client"""
    print("Echo found!")
    client_socket.send(b'Echoing')
    client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Host should be 'localhost'
host = 'localhost'

port = 10145

# Binding to port
server_socket.bind((host, port))
server_socket.listen(1)

# Server-side output
print("Listening on: " + str(host))
print("Port: " + str(port))
print("Available items: download, info, link, page1, echo, exit")
print("Waiting for client:")

while True:
    client_socket, addr = server_socket.accept()
    data = client_socket.recv(1024).decode()

    decoded_data = str(data).split('\n')
    print()  # Empty line
    print("Recv Data: " + str(data).split('\n')[0])
    print(decoded_data[1])  # Produces 'host' line
    print(decoded_data[2])  # Produces 'user-agent' line

    # The command the client is requesting
    command = decoded_data[0].split()[1][1:]

    if command == 'info':
        to_info_page()
    elif command == 'page1':
        produce_page1()
    elif command == 'link':
        to_download_link()
    elif command == 'download':
        distribute_download()
    elif command == 'echo':
        send_echo()
    elif command == 'exit':
        print("Now exiting...")
        client_socket.send(b'Exiting now!')
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()
        break
    else:
        client_socket.send(b'Not a valid link. Try: info, download, link, '
                           b'page1, echo, exit')
        print("Client requested an unavailable page")
        client_socket.close()
# If 'exit' is requested by the client, the server socket will close
server_socket.close()
