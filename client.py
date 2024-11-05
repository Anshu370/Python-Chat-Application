import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, ttk
from plyer import notification

# Client setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 1234))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'USERNAME':
                client.send(username.encode('utf-8'))
            elif "typing" in message:
                typing_status_label.config(text=message)
            else:
                chat_box.config(state=tk.NORMAL)
                # Notification for join/leave messages
                if "joined the chat" in message or "left the chat" in message:
                    notification.notify(
                        title='Chat Notification',
                        message=message,
                        timeout=5
                    )
                if message.startswith(username):
                    chat_box.insert(tk.END, message + '\n', 'self')
                else:
                    chat_box.insert(tk.END, message + '\n', 'other')
                    # Show notification only if it's not the user's own message
                    notification.notify(
                        title='Chat Application',
                        message=message,
                        timeout=2
                    )
                chat_box.config(state=tk.DISABLED)
                chat_box.yview(tk.END)
        except Exception as e:
            print(f'An error occurred! {e}')
            client.close()
            break

def send_message(event=None):
    message = message_entry.get()
    message_entry.set('')
    if message:
        message = f'{username}: {message}'
        client.send(message.encode('utf-8'))
        stop_typing()

def on_typing(event=None):
    try:
        typing_message = f"{username} is typing..."
        client.send(typing_message.encode('utf-8'))
    except:
        pass

def stop_typing(event=None):
    try:
        typing_message = f"{username} stopped typing."
        client.send(typing_message.encode('utf-8'))
    except:
        pass

# GUI setup
root = tk.Tk()
root.title("Chat Application")
root.geometry("600x500")
root.resizable(False, False)

# Custom Styles
style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10, background="#4CAF50", foreground="green")
style.map("TButton", background=[("active", "#45a049")])
style.configure("TEntry", font=("Segoe UI", 10), padding=10)
style.configure("TLabel", font=("Segoe UI", 10))

# Header Frame for typing status
header_frame = ttk.Frame(root, padding="10")
header_frame.pack(fill=tk.X)

# Label to show typing status
typing_status_label = ttk.Label(header_frame, text="", style="TLabel")
typing_status_label.pack(anchor=tk.W)

# Body Frame for chat and input
body_frame = ttk.Frame(root, padding="10")
body_frame.pack(fill=tk.BOTH, expand=True)

# Chat box with rounded corners and a modern font
chat_box = scrolledtext.ScrolledText(body_frame, height=20, width=70, state=tk.DISABLED, wrap=tk.WORD, font=("Segoe UI", 10), bg="#ffffff", fg="#333333", relief=tk.FLAT, borderwidth=5)
chat_box.pack(fill=tk.BOTH, expand=True)
chat_box.config(cursor="arrow")

# Adding tags for different styles
chat_box.tag_config('self', background="#e0f7fa", foreground="#00695c")
chat_box.tag_config('other', background="#fff9c4", foreground="#f57f17")

# User input frame with custom background
input_frame = ttk.Frame(root, padding="15")
input_frame.pack(fill=tk.X)

# Message entry field with rounded corners
message_entry = tk.StringVar()
entry_field = ttk.Entry(input_frame, textvariable=message_entry, width=50, style="TEntry")
entry_field.bind("<Return>", send_message)
entry_field.bind("<KeyPress>", on_typing)
entry_field.bind("<KeyRelease>", stop_typing)
entry_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

# Send button with modern design
send_button = ttk.Button(input_frame, text="Send", command=send_message, style="TButton")
send_button.pack(side=tk.RIGHT, padx=10)

# Username dialog
username = simpledialog.askstring("Username", "Enter your username", parent=root)

# Start receiving messages in a separate thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Run the Tkinter main loop
root.mainloop()
