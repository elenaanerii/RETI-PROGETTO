#!/usr/bin/env python3

#NERI ELENA MATRICOLA 0001098044

"""
TRACCIA 1: SISTEMA DI CHAT CLIENT-SERVER: GESTISCE PII' CLIENT 
CONTEMPORANEAMENTE, GLI UTENTI POSSONO INVIARE E RICEVERE MESSAGGI
IN UNA CHATROOM CONDIVISA
"""

import os
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys
import signal


def inbound_connection():  
    while True:
        try:
            client, client_address = SERVER.accept()
            print(f"{client_address[0]}:{client_address[1]} is connecting on server")
            client.send(bytes("WRITE YOUR NAME TO START!", "utf8"))
            addresses[client] = client_address
            Thread(target=manageClient, args=(client,)).start()
        except Exception as e:
            print("Errore durante l'accettazione di una connessione: ", e)
            break

def manageClient(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = "WELCOME %s! PRESS BUTTON QUIT TO LEFT THE CHATROOM" % name
    client.send(bytes(welcome, "utf8"))
    message = f"{name} JOINED THE CHAT!"
    broadcast(bytes(message, "utf8"))
    clients[client] = name

    while True:
        try:
            message = client.recv(BUFSIZ)
            if not message:
                break
            if message == bytes("{quit}", "utf8"):
                del clients[client]
                broadcast(bytes(f"{name} LEFT THE CHAT!", "utf8"))
                client.close()
                break
            else:
                broadcast(message, name+": ")
        except ConnectionResetError:
            del clients[client]
            broadcast(bytes(f"{name} LEFT THE CHAT!", "utf8"))
            client.close()
            break
        except Exception as e:
            print("Errore durante la ricezione del messaggio: ", e)
            break
    check_empty_clients()

def broadcast(message, prefix=""):
    for client in clients:
        client.send(bytes(prefix, "utf8")+message)

def check_empty_clients():
    if not clients:
        print("All clients have left. Server is closing...")
        os._exit(0)

clients = {}
addresses = {}
BUFSIZ=1024
HOST = ''
PORT = 53000
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def sigint_handler(sig, frame):
    print('SERVER IS CLOSING...')
    SERVER.close()
    sys.exit(0)

if __name__ == "__main__":
    try:
        signal.signal(signal.SIGINT, sigint_handler)
        SERVER.listen(5) 
        print("CONNECTION LOADING...")
        inbound_connection()
    except Exception as e:
        print("Errore durante l'avvio del server: ", e)
    finally:
        SERVER.close()