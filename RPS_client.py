"""
Cyber-Kaeh
12/9/23
RPS_client.py: The client side program for the rock, paper, scissors game. Contains a GUI for the user
to play the game and show the status of the game.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import socket
import threading
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Client: Rock / Paper / Scissors")
root.configure(bg="#FFE666")
style = ttk.Style()
style.configure('TLabelframe', background='#FFE666')
style.configure('TLabel', foreground='blue', background='#FFE666', font=("Helvetica", 14, 'bold'))
style.configure('TLabelframe.Label', font=("Helvetica", 14), foreground="blue", background="#FFE666")


def get_image_path(result):
    if result == 'rock':
        return 'rock_pic.png'
    elif result == 'paper':
        return 'paper_pic.png'
    elif result == 'scissors':
        return 'scissors_pic.png'
    else:
        return 'rps_start.png'


def resize_img(img_path, size):
    image = Image.open(img_path)
    image_res = image.resize(size, resample=Image.LANCZOS)
    return image_res


def update_player_image(selection):
    file_path = get_image_path(selection)
    img = resize_img(file_path, (220, 220))
    photo = ImageTk.PhotoImage(img)

    # Update the image on the label
    player_image.config(image=photo)
    player_image.image = photo


def update_opp_image(selection):
    file_path = get_image_path(selection)
    img = resize_img(file_path, (220, 220))
    photo = ImageTk.PhotoImage(img)

    # Update the image on the label
    opponent_image.config(image=photo)
    opponent_image.image = photo


# Add a label frame to hold the image
player_image_frame = ttk.LabelFrame(root, text="Your throw")
player_image_frame.grid(row=0, column=0)
# Add a label to display the image
start_img = resize_img('rps_start.png', (220, 220))
start_photo = ImageTk.PhotoImage(start_img)
player_image = ttk.Label(player_image_frame, image=start_photo)
player_image.pack(pady=10)
# player_image.image = player_image

# The VS label
vs_label = ttk.Label(root, text="VS")
vs_label.grid(row=0, column=1)

# The opponents throw label frame
opponent_label_frame = ttk.LabelFrame(root, text="Opponent's Throw")
opponent_label_frame.grid(row=0, column=2)

opp_start_img = resize_img('rps_start.png', (220, 220))
opp_start_photo = ImageTk.PhotoImage(opp_start_img)
opponent_image = ttk.Label(opponent_label_frame, image=opp_start_photo)
opponent_image.pack(pady=10)


# Open the pictures to use as buttons
rock_button_pic = resize_img('rock_pic.png', (175, 175))
rock_button_photo = ImageTk.PhotoImage(rock_button_pic)

paper_button_pic = resize_img('paper_pic.png', (175, 175))
paper_button_photo = ImageTk.PhotoImage(paper_button_pic)

scissor_button_pic = resize_img('scissors_pic.png', (175, 175))
scissor_button_photo = ImageTk.PhotoImage(scissor_button_pic)

# Make the buttons for the user to select their throw
rock_button = tk.Button(root, command=lambda: throw_rock(), image=rock_button_photo, background='#FFE666')
rock_button.grid(row=1, column=0, pady=10)

paper_button = tk.Button(root, command=lambda: throw_paper(), image=paper_button_photo, background='#FFE666')
paper_button.grid(row=1, column=1, pady=10)

scissor_button = tk.Button(root, command=lambda: throw_scissors(), image=scissor_button_photo, background='#FFE666')
scissor_button.grid(row=1, column=2, pady=10)

# Status bar to display information to the user
status_bar = ttk.Label(text="Welcome! Enter name below and click connect to get started.")
status_bar.grid(row=2, columnspan=3)


# Entry box for client name and connect button
# Add an entry and button to simulate getting a result
bottom_frame = ttk.Frame(root)
bottom_frame.grid(row=3, column=0, columnspan=4)

name_entry = tk.Entry(bottom_frame)
name_entry.grid(row=0, column=0, columnspan=3, sticky=tk.EW)

connect_button = tk.Button(bottom_frame, text="Connect", command=lambda: connect())
connect_button.grid(row=0, column=3)


"""Client Logic"""
# Network globals
client = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 2001

your_details = {"name": "Ant", "wins": 0, "loses": 0}
list_labels = []


def connect():
    global your_details
    if len(name_entry.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        your_details["name"] = name_entry.get()
        connect_to_server(name_entry.get())


def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client.connect((HOST_ADDR, HOST_PORT))
        print("Client connected")
        client.sendall(name.encode())
        # start a thread to keep receiving message from server
        threading._start_new_thread(receive_message_from_server, (client, "m"))
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(
            HOST_PORT) + " Server may be Unavailable. Try again later")


def receive_message_from_server(sck, m):
    global status_bar
    # while True:
    from_server = sck.recv(4096)

    if from_server.startswith("Welcome".encode()):
        status_bar["text"] = from_server.decode()


def throw_rock():
    global client
    msg = "throw rock"
    client.send(msg.encode())
    opp_throw = client.recv(1024).decode()

    # Update the pictures after receiving choice from server
    update_player_image('rock')
    update_opp_image(opp_throw)

    if opp_throw == 'rock':
        # draw
        status_bar["text"] = "Darn! it's a draw!"
        status_bar.config(foreground='gray')
    elif opp_throw == 'scissors':
        # win
        status_bar["text"] = "Woah! You won!"
        status_bar.config(foreground='green')
    elif opp_throw == 'paper':
        # lose
        status_bar["text"] = "Uh-oh! You lost."
        status_bar.config(foreground='red')

def throw_paper():
    global client
    msg = "throw paper"
    client.send(msg.encode())
    opp_throw = client.recv(1024).decode()

    # Update the pictures after receiving choice from server
    update_player_image('paper')
    update_opp_image(opp_throw)

    if opp_throw == 'paper':
        # draw
        status_bar["text"] = "Drat! We tied!"
        status_bar.config(foreground='gray')
    elif opp_throw == 'rock':
        # win
        status_bar["text"] = "Nice! You won!"
        status_bar.config(foreground='green')
    elif opp_throw == 'scissors':
        # lose
        status_bar["text"] = "Aw.. you lost. Try again!"
        status_bar.config(foreground='red')


def throw_scissors():
    global client
    msg = "throw scissors"
    client.send(msg.encode())
    opp_throw = client.recv(1024).decode()

    # Update the pictures after receiving choice from server
    update_player_image('scissors')
    update_opp_image(opp_throw)

    if opp_throw == 'scissors':
        # draw
        status_bar["text"] = "A draw?! Go again?"
        status_bar.config(foreground='gray')
    elif opp_throw == 'paper':
        # win
        status_bar["text"] = "Congrats! You won!"
        status_bar.config(foreground='green')
    elif opp_throw == 'rock':
        # lose
        status_bar["text"] = "You lost. Try again!"
        status_bar.config(foreground='red')


def on_closing():
    try:
        client.send('disconnect'.encode())
    except (socket.error, ConnectionResetError, AttributeError):
        print("Connection error, server may have already closed connection.")
    finally:
        try:
            client.close()
        except AttributeError:
            pass
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
