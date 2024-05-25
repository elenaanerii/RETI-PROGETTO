#!/usr/bin/env python3

#NERI ELENA MATRICOLA 0001098044

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt
import sys

def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf8")
            if message:
                message_list.insert(tkt.END, message)
                message_list.see(tkt.END)
        except OSError:  # Gestione errore di connessione interrotta
            break

def stop():
    try:
        client_socket.close()
    except Exception as e:
        print("Errore durante la chiusura del socket: ", e)
    try:
        window.destroy()
    except tkt.TclError as e:
        if "can't invoke" in str(e):
            # Se l'errore è "can't invoke", significa che la finestra è già stata distrutta, quindi non fare nulla
            pass
        else:
            # Altrimenti, stampa l'errore
            print("Errore durante la chiusura della finestra: ", e)
        

def send(event=None):
    message = mymessage.get()
    mymessage.set("")
    try:
        if message:
            client_socket.send(bytes(message, "utf8"))
    except ConnectionResetError:
        stop()

def check_window_count():
    global open_windows
    open_windows -= 1
    # Controlla il numero di finestre aperte
    if open_windows == 0:
        sys.exit(0)

def start():
    global client_socket, window, message_list, mymessage, open_windows
    open_windows=1
    HOST = 'localhost'
    PORT = 53000

    ADDR = (HOST, PORT)
    client_socket = socket(AF_INET, SOCK_STREAM)
    try:
        client_socket.connect(ADDR)
    except Exception as e:
        print("Errore durante la connessione al server: ", e)
        return
    
    window = tkt.Tk()
    window.title("CHATROOM PROGETTO") 
    window.configure(bg="purple")
    messages_frame = tkt.Frame(window)
    mymessage = tkt.StringVar()
    mymessage.set(" ")
    scrollbar = tkt.Scrollbar(messages_frame)
    message_list = tkt.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set, bg="lightpink", fg="black", font=("Helvetica", 12))
    scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
    message_list.pack(side=tkt.LEFT, fill=tkt.BOTH, expand=True)
    messages_frame.pack(padx=10, pady=10, expand=True, fill=tkt.BOTH)
    entry_field = tkt.Entry(window, textvariable=mymessage, font=("Helvetica", 12))
    entry_field.bind("<Return>", send)
    entry_field.pack(padx=10, pady=10, fill=tkt.X)
    send_button = tkt.Button(window, text="SEND", command=send, font=("Helvetica", 12), bg="blue", fg="white")
    send_button.pack(pady=10)
   
    close_button = tkt.Button(window, text="QUIT", command=stop, font=("Helvetica", 12), bg="red", fg="white")
    close_button.pack(pady=10)

    window.protocol("WM_DELETE_WINDOW", stop)
    open_windows +=1

    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkt.mainloop()

if __name__ == "__main__":
    try:
        start()
    except Exception as e:
        print("Errore durante l'esecuzione del client: ", e)
    finally:
        stop()
        sys.exit(0)