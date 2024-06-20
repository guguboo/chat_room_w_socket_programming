from tkinter import *
from tkinter import messagebox

# List to store the chat rooms
chat_rooms = []

def create_chat_room():
    # Create a new window for creating a chat room
    create_window = Toplevel(window)
    create_window.title("Create Chat Room")
    create_window.geometry(f"{lebar}x{tinggi}+{x}+{y}")

    Label(create_window, text="Chat Room Name:").pack(pady=10)
    chat_room_name = Entry(create_window)
    chat_room_name.pack(pady=10)

    Label(create_window, text="Description:").pack(pady=10)
    description = Entry(create_window)
    description.pack(pady=10)

    def submit():
        room_name = chat_room_name.get()
        desc = description.get()
        if room_name:
            chat_rooms.append(room_name)  # Add the new room name to the list
            messagebox.showinfo("Success", f"Chat room '{room_name}' created successfully!")
            create_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Chat room name is required!")

    Button(create_window, text="Create", command=submit).pack(pady=20)
    Button(create_window, text="Cancel", command=create_window.destroy).pack(pady=10)

def see_chat_rooms():
    # Create a new window to display available chat rooms
    rooms_window = Toplevel(window)
    rooms_window.title("Available Chat Rooms")
    rooms_window.geometry(f"{lebar}x{tinggi}+{x}+{y}")

    Label(rooms_window, text="Available Chat Rooms:").pack(pady=10)
    listbox = Listbox(rooms_window)
    listbox.pack(pady=10)

    for room in chat_rooms:
        listbox.insert(END, room)

    Button(rooms_window, text="Back", command=rooms_window.destroy).pack(pady=10)

window = Tk()
lebar = 350
tinggi = 500

screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()

x = int((screenwidth / 2) - (lebar / 2))
y = int((screenheight / 2) - (tinggi / 2))

window.title("Jarkom Chatting")
window.geometry(f"{lebar}x{tinggi}+{x}+{y}")

Button(window, text="Create Chat Room", command=create_chat_room).pack(pady=20)
Button(window, text="See Available Chat Rooms", command=see_chat_rooms).pack(pady=20)

window.mainloop()
