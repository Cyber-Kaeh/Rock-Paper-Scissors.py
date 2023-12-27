"""
Cyber-Kaeh
12/11/23
RPS_server.py: is the server side program that facilitates the client program. This program will just start
a server for clients to connect to then send back random rock, paper, scissor choices to allow the user
to play against. It onlu allows for multiple clients to connect simultaneously but I would like to implement
a client vs. client multiplayer feature. 
"""

import tkinter as tk
import socket
import threading
from time import sleep
import random

root = tk.Tk()
root.title("Server: Rock / Paper / Scissors")

# Start and Stop buttons for the server
top_frame = tk.Frame(root)
top_frame.grid(row=0, column=0, columnspan=4)

start_button = tk.Button(top_frame, text="Start", command=lambda: start_server())
start_button.grid(row=0, column=1, pady=10)

stop_button = tk.Button(top_frame, text="Stop", command=lambda: stop_server(), state=tk.DISABLED)
stop_button.grid(row=0, column=2, pady=10)

# Middle frame to hold host/port information
middle_frame = tk.Frame(root)
middle_frame.grid(row=1, column=0, columnspan=4)

label_host = tk.Label(middle_frame, text="Host: 0.0.0.0")
label_host.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky=tk.E)

label_port = tk.Label(middle_frame, text="Port: 0000")
label_port.grid(row=0, column=2, columnspan=2, pady=10, padx=10, sticky=tk.W)

# Client frame shows connected clients
client_frame = tk.Frame(root)
client_frame.grid(row=2, column=0, columnspan=4)
label_client = tk.Label(client_frame, text="/\/\/\-Current Players-/\/\/\\")
label_client.grid(row=0, column=0)

scroll_bar = tk.Scrollbar(client_frame)
scroll_bar.grid(row=1, column=4, sticky=tk.NS)
display_client = tk.Text(client_frame, height=10, width=30)
display_client.grid(row=1, column=0, sticky=tk.EW)
scroll_bar.config(command=display_client.yview)
display_client.config(yscrollcommand=scroll_bar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")


# Set the host/port numbers and initialize lists to hold data
server = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 2001
client_name = " "
clients = []
clients_names = []
player_data = []
server_choices = ['rock', 'paper', 'scissors']

# Start server button function
def start_server():
    global server, HOST_ADDR, HOST_PORT # code is fine without this
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(10)  # server is listening for client connection

    threading._start_new_thread(accept_clients, (server, " "))

    label_host["text"] = "Address: " + HOST_ADDR
    label_port["text"] = "Port: " + str(HOST_PORT)


# Stop server button function
def stop_server():
    global server
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

    if server:
        server.close()
        print('Server shutting down...')


# Function to accept new clients
def accept_clients(the_server, y):
    while True:
        client, addr = the_server.accept()
        clients.append(client)

        # use a thread so as not to clog the gui thread
        threading._start_new_thread(send_receive_client_message, (client, addr))


# Function to send/receive data
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, player_data, server_choices
    client_msg = " "

    # send welcome message to client
    client_name = (client_connection.recv(4096)).decode()
    clients_names.append(client_name)    # append new client to clients list
    client_connection.send(("Welcome " + client_name + "! Let's play!").encode())

    update_client_names_display(clients_names)  # update client names display

    while True:
        # receive throw from client
        data = client_connection.recv(4096).decode()

        # receive message to keep playing
        if data.startswith("throw"):
            client_throw = data[6:]
            server_throw = random.choice(server_choices)
            client_connection.send(server_throw.encode())
        # receive disconnect message
        elif data.startswith("disconnect"):
            handle_disconnect(client_connection)
            update_client_names_display(clients_names)
            break

    # find the client index then remove from current players display
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]

    update_client_names_display(clients_names)  # update client names display


def handle_disconnect(client_connection):
    print('Client disconnected')
    client_connection.close()


# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Update client name display when a new client connects OR
# When a connected client disconnects
def update_client_names_display(name_list):
    display_client.config(state=tk.NORMAL)
    display_client.delete('1.0', tk.END)
    print(name_list)
    for c in name_list:
        display_client.insert(tk.END, c+"\n")
    display_client.config(state=tk.DISABLED)




root.mainloop()
