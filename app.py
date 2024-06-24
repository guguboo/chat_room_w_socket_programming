import sys
from tkinter import *
from tkinter import messagebox
import re
from client import Client
import mysql.connector

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


class ChatWindow:
    def __init__(self):
        self.chat_rooms = []
        self.room_name = ""
        self.room_id = ""
        self.room_owner = ""
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    # Fungsi untuk koneksi ke database
    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='jarkom',
                user='root',
                password=''
            )
            return connection
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def _setup_main_window(self):
        self.window.title("Chatroom")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        self.head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="Selamat Datang! Silakan Masukan Username!",
                            font=FONT_BOLD, pady=10)

        self.head_label.place(relwidth=1)

        #divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.changeableWindow = Label(self.window, bg=BG_COLOR)
        self.changeableWindow.place(rely=0.1, relwidth=1, relheight=1)

        self._login_window()

    def _login_window(self):
        self.clear_all()

        # Username
        user_label = Label(self.changeableWindow, text="Username", font=FONT_BOLD, anchor='w', bg=BG_COLOR, fg=TEXT_COLOR)
        user_label.place(relx=0.02, relwidth=0.4)
        self.user_box = Entry(self.changeableWindow, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.user_box.place(relx=0.02, rely=0.05, relheight=0.06, relwidth=0.3)
        self.user_box.bind("<Return>", self.on_enter_username)

        # Password
        pass_label = Label(self.changeableWindow, text="Password", font=FONT_BOLD, anchor='w', bg=BG_COLOR, fg=TEXT_COLOR)
        pass_label.place(relx=0.02, rely=0.15, relwidth=0.4)
        self.pass_box = Entry(self.changeableWindow, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, show = "*")
        self.pass_box.place(relx=0.02, rely=0.2, relheight=0.06, relwidth=0.3)
        self.pass_box.bind("<Return>", self.on_enter_username)

        # OK
        send_button = Button(self.changeableWindow, text="OK", font=FONT_BOLD, width=20, bg=BG_GRAY,
                            command=lambda: self.on_enter_username(None))
        send_button.place(relx=0.34, rely=0.3, relheight=0.06, relwidth=0.1)

        # Register
        register_button = Button(self.changeableWindow, text="Register", font=FONT_BOLD, width=20, bg=BG_GRAY,
                                command=self._register_window)
        register_button.place(relx=0.45, rely=0.3, relheight=0.06, relwidth=0.15)

        self.user_box.focus()

    def on_enter_username(self, event):
        self.username = self.user_box.get()
        self.password = self.pass_box.get()
        authenticated = self._authenticate_user()

        err_label = Label(self.changeableWindow, font=FONT, fg="red", bg=BG_COLOR, anchor='w')
        err_label.place(relx=0.02, rely=0.1, relwidth=0.7)
        if not authenticated:
            err_label.config(text="Username atau Password Salah")
        else:
            self.main_menu()
            # self.client = Client(self.username, self)
            # self._chat_window()

    def _authenticate_user(self):
        if not self.username or not self.password:
            return False
        else:
            connection = self.connect_to_database()

            if connection.is_connected():
                cursor = connection.cursor()

                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM users WHERE username = %s AND password = %s"
                cursor.execute(query, (self.username, self.password))
                user = cursor.fetchone()
                cursor.close()
                connection.close()

                return user is not None

    def _register_window(self):
        self.clear_all()

        self.head_label.config(text="Register New User")

        # Username
        user_label = Label(self.changeableWindow, text="Username", font=FONT_BOLD, anchor='w', bg=BG_COLOR, fg=TEXT_COLOR)
        user_label.place(relx=0.02, relwidth=0.4, rely=0.02)
        self.reg_user_box = Entry(self.changeableWindow, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.reg_user_box.place(relx=0.02, rely=0.07, relheight=0.06, relwidth=0.3)
        self.reg_user_box.bind("<Return>", self.on_register_user)

        # Password
        pass_label = Label(self.changeableWindow, text="Password", font=FONT_BOLD, anchor='w', bg=BG_COLOR, fg=TEXT_COLOR)
        pass_label.place(relx=0.02, relwidth=0.4, rely=0.15)
        self.reg_pass_box = Entry(self.changeableWindow, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, show="*")
        self.reg_pass_box.place(relx=0.02, rely=0.2, relheight=0.06, relwidth=0.3)
        self.reg_pass_box.bind("<Return>", self.on_register_user)

        # Register
        register_button = Button(self.changeableWindow, text="Register", font=FONT_BOLD, width=20, bg=BG_GRAY,
                                command=lambda: self.on_register_user(None))
        register_button.place(relx=0.34, rely=0.3, relheight=0.06, relwidth=0.15)
        self.reg_user_box.focus()

    def on_register_user(self, event):
        self.reg_username = self.reg_user_box.get()
        self.reg_password = self.reg_pass_box.get()
        registered = self._register_user()

        err_label = Label(self.changeableWindow, font=FONT, fg="red", bg=BG_COLOR, anchor='w')
        err_label.place(relx=0.02, rely=0.1, relwidth=0.5)
        if not registered:
            err_label.config(text="Registration failed. Try again.")
        else:
            self.head_label.config(text="Registration Successful! Please Login.")
            self._login_window()

    def _register_user(self):
        if not self.reg_username or not self.reg_password:
            return False
        try:
            connection = self.connect_to_database()
            if connection.is_connected():
                cursor = connection.cursor()

                # Cek apakah sudah ada username tersebut
                query_check = "SELECT * FROM users WHERE username = %s"
                cursor.execute(query_check, (self.reg_username,))
                existing_user = cursor.fetchone()

                if existing_user:
                    return False

                query = "INSERT INTO users (username, password) VALUES (%s, %s)"

                cursor.execute(query, (self.reg_username, self.reg_password))
                connection.commit()
                cursor.close()
                connection.close()
                return True
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False


    def _chat_window(self):
        #text widget
        self.clear_all()
        self.head_label.config(text=self.room_name)

        self.user_list = Listbox(self.changeableWindow, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        self.user_list.place(relwidth=0.3, relheight=0.745, rely=0)

        self.text_widget = Text(self.changeableWindow, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.960)
        scrollbar.configure(command=self.text_widget.yview)

        #btm label
        bottom_label = Label(self.changeableWindow, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.745)

        #buat ketik
        self.msg_box = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_box.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_box.focus()
        self.msg_box.bind("<Return>", self.on_enter_msg)

        #send btn
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                            command=lambda: self.on_enter_msg())
        self.back_btn = Button(self.window, text="Back", font=FONT_BOLD, bg=BG_GRAY,
                            command=lambda: self.back_to_main_menu())
        members_button = Button(self.changeableWindow, text="Members", command=self.show_members, font=FONT_BOLD,
                                width=20, bg=BG_GRAY)

        self.back_btn.place(relx=0.02, rely=0.008)
        members_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    def show_members(self):
        connection = self.connect_to_database()
        cursor = connection.cursor()
        # Create a new window to display members
        self.members_window = Toplevel(self.window)
        self.members_window.title("Members in Chat Room")
        width = 350
        height = 500

        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()

        x = int((screenwidth / 2) - (width / 2))
        y = int((screenheight / 2) - (height / 2))
        self.members_window.geometry(f"{width}x{height}+{x}+{y}")

        Label(self.members_window, text=f"Members in Room '{self.room_name}':", font=FONT_BOLD).pack(pady=10)

        cursor.execute("SELECT Room_Id FROM chat_room WHERE Room_Name = %s", (self.room_name,))
        self.room_id = cursor.fetchone()[0]
        Label(self.members_window, text=f"Room Id: '{self.room_id}':", font=FONT_BOLD).pack(pady=10)

        # Create a listbox to display members
        listbox = Listbox(self.members_window)
        listbox.pack(pady=10)

        # Fetch members from database
        cursor.execute("SELECT member.username FROM member WHERE Room_Id = %s", (self.room_id,))
        members = cursor.fetchall()

        cursor.execute( "SELECT username FROM chat_room WHERE Room_Name = %s", (self.room_name,))
        owner = cursor.fetchone()
        self.room_owner = owner[0]
        connection.close()

        # Insert members into listbox
        for member in members:
            listbox.insert(END, member[0])

        # Function to handle listbox selection
        def on_select(event):
            selected_member = listbox.get(listbox.curselection())
            print(selected_member)
            print(self.username)
            print(self.room_owner)
            if self.username == self.room_owner:
                print("masuk")
                if selected_member != self.username and selected_member != self.room_owner:
                    self.prompt_delete_member(selected_member, self.room_name)
                elif selected_member == self.username:
                    messagebox.showwarning("Warning", "You cannot delete yourself.")

        listbox.bind('<<ListboxSelect>>', on_select)

        Button(self.members_window, text="Leave", command=lambda: self.prompt_leave(self.room_name)).pack(pady=10)
        # Button to close the window
        Button(self.members_window, text="Close", command=self.members_window.destroy).pack(pady=10)

    def prompt_leave(self, room_name):
        answer = messagebox.askyesno("Leave Room", f"Are you sure you want to leave room {room_name}?")
        if answer:
            self.leave_room(self.username, room_name)

    def leave_room(self, member, room_name):
        connection = self.connect_to_database()
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT Room_Id FROM chat_room WHERE Room_Name = %s"
            cursor.execute(query, (room_name,))
            id = (cursor.fetchone())[0]

            query = "SELECT username FROM chat_room WHERE Room_Name = %s"
            cursor.execute(query, (room_name,))
            usn = (cursor.fetchone())[0]

            if usn:
                query = "DELETE FROM chat_room WHERE username = %s AND Room_Id = %s"
                cursor.execute(query, (member, id))

                query = "DELETE FROM member WHERE Room_Id = %s"
                cursor.execute(query, (id,))
                connection.commit()
            else:
                query = "DELETE FROM member WHERE username = %s AND Room_Id = %s"
                cursor.execute(query, (member, id))
                connection.commit()

            self.members_window.destroy()
            self.back_to_main_menu()

            cursor.close()
            connection.close()

    def prompt_delete_member(self, member, room_name):
        answer = messagebox.askyesno("Delete Member", f"Are you sure you want to delete {member}?")
        if answer:
            self.delete_member(member, room_name)

    def delete_member(self, member, room_name):
        connection = self.connect_to_database()
        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT Room_Id FROM chat_room WHERE Room_Name = %s"
            cursor.execute(query, (room_name,))
            id = (cursor.fetchone())[0]
            query = "DELETE FROM member WHERE username = %s AND Room_Id = %s"
            cursor.execute(query, (member, id))
            connection.commit()
            cursor.close()
            connection.close()
            self.show_members()

    def update_user_list(self, usernames):
        self.user_list.delete(0, END)
        for username in usernames:
            self.user_list.insert(END, username)

    def notify_user_joined(self, username):
        self.insert_message(f"{username} has joined the chat.")

    def on_enter_msg(self, event=None):
        msg = self.msg_box.get()
        self.client.send_message(msg)
        self.msg_box.delete(0, END)  # Clear the message box after sending
        return msg

    def back_to_main_menu(self):
        self.back_btn.destroy()
        self.client.close_socket()
        self.main_menu()

    def insert_message(self, msg):
        if not msg:
            return

        msg_box_initiated = False

        while not msg_box_initiated:
            try:
                self.msg_box.delete(0, END)
                msg_box_initiated = True
            except:
                pass
        msg1 = msg + "\n\n"
        self.text_widget.configure(cursor="arrow", state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        self.text_widget.see(END)

    def clear_all(self):
        # Get all child widgets of the window and destroy them
        for widget in self.changeableWindow.winfo_children():
            widget.destroy()


    #main menu
    def create_chat_room(self):
        create_window = Toplevel(self.window)
        create_window.title("Create Chat Room")
        lebar = 350
        tinggi = 500

        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()

        x = int((screenwidth / 2) - (lebar / 2))
        y = int((screenheight / 2) - (tinggi / 2))
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
            if re.match("^[A-Za-z0-9 ]+$", room_name):
                connection = self.connect_to_database()

                cursor = connection.cursor()

                try:
                    # Insert new chat room
                    cursor.execute(
                        "INSERT INTO chat_room (username, Room_Name, Created_At) VALUES (%s, %s, NOW())",
                        (self.username, room_name)
                    )
                    connection.commit()

                    # Fetch the Room_Id of the newly created chat room
                    cursor.execute("SELECT Room_Id FROM chat_room WHERE Room_Name = %s", (room_name,))
                    room_id = cursor.fetchone()

                    if room_id:
                        room_id = room_id[0]

                        # Insert into member table
                        cursor.execute(
                            "INSERT INTO member (username, Room_Id) VALUES (%s, %s)",
                            (self.username, room_id)
                        )
                        connection.commit()

                        self.chat_rooms.append(room_name)
                        messagebox.showinfo("Success", f"Chat room '{room_name}' created successfully!")
                        create_window.destroy()
                        self.client = Client(self.username, self, room_name)
                        self.room_name = room_name
                        self._chat_window()
                    else:
                        messagebox.showwarning("Error", "Failed to fetch Room_Id for the new chat room!")

                except mysql.connector.Error as e:
                    connection.rollback()
                    print(f"Error: {e}")
                    messagebox.showerror("Database Error", f"An error occurred: {e}")
                finally:
                    cursor.close()
                    connection.close()
            else:
                messagebox.showwarning("Input Error", "Chat room name invalid!")

        Button(create_window, text="Create", command=submit).pack(pady=20)
        Button(create_window, text="Cancel", command=create_window.destroy).pack(pady=10)

    def creating_room_handle(self, msg):
        print(msg)
        if msg == "err":
            messagebox.showwarning("Room Error", "Chat Room Dengan Nama Tersebut Sudah Ada!")
        else:
            self._chat_window()
    def see_chat_rooms(self):
    # Create a new window to display available chat rooms
        rooms_window = Toplevel(self.window)
        rooms_window.title("Available Chat Rooms")
        self.room_window = rooms_window
        lebar = 350
        tinggi = 500

        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()

        x = int((screenwidth / 2) - (lebar / 2))
        y = int((screenheight / 2) - (tinggi / 2))
        rooms_window.geometry(f"{lebar}x{tinggi}+{x}+{y}")

        Label(rooms_window, text="Available Chat Rooms:").pack(pady=10)
        listbox = Listbox(rooms_window)
        listbox.pack(pady=10)
        listbox.bind('<<ListboxSelect>>', self.on_listbox_select)

        connection = self.connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT Room_Name FROM chat_room JOIN member ON chat_room.Room_Id = member.Room_Id WHERE member.username = %s", (self.username,))
        chat_rooms = cursor.fetchall()
        connection.close()

        self.chat_rooms = [room[0] for room in chat_rooms]

        for room in self.chat_rooms:
            listbox.insert(END, room)

        def open_chat(event):
            selected_room = listbox.get(listbox.curselection())
            self.client = Client(self.username, self, selected_room)
            self.room_name = selected_room
            self._chat_window()
            rooms_window.destroy()

        listbox.bind('<<ListboxSelect>>', open_chat)
        Button(rooms_window, text="Back", command=rooms_window.destroy).pack(pady=10)

    def on_listbox_select(self, event):
        #append ke DB juga

        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            selected_room = event.widget.get(index)
            print(f"Selected room: {selected_room}")
            self.client = Client(self.username, self, selected_room)
            self.room_name = selected_room
            self._chat_window()
            self.room_window.destroy()

    def main_menu(self):
        self.clear_all()
        self.head_label.config(text="Main Menu - Chatroom Vico, Andrea, Nirvana")
        create_room = Button(self.changeableWindow, text="Create Chat Room", command=self.create_chat_room, font=FONT_BOLD, width=20, bg=BG_GRAY)
        create_room.pack(pady=10)
        see_list = Button(self.changeableWindow, text="See All Chat Rooms", command=self.see_chat_rooms, font=FONT_BOLD, width=20, bg=BG_GRAY)
        see_list.pack(pady=10)
        join_room = Button(self.changeableWindow, text="Join Chat Room", command=self.join_chat_room, font=FONT_BOLD,
                        width=20, bg=BG_GRAY)
        join_room.pack(pady=10)

    def _join_chat_room_by_id(self, room_id):
        try:
            connection = self.connect_to_database()
            cursor = connection.cursor()

            # Check if the room exists
            cursor.execute("SELECT * FROM chat_room WHERE Room_Id = %s", (room_id,))
            room = cursor.fetchone()
            if room:
                # Check if the user is already in the room
                cursor.execute(
                    "SELECT * FROM member WHERE username = %s AND Room_Id = %s",
                    (self.username, room_id)
                )
                user_in_room = cursor.fetchone()
                if not user_in_room:
                    # Add user to chat room
                    cursor.execute(
                        "INSERT INTO member (username, Room_Id) VALUES (%s, %s)",
                        (self.username, room_id)
                    )
                    connection.commit()

                # Fetch room name for display purposes
                cursor.execute("SELECT Room_Name FROM chat_room WHERE Room_Id = %s", (room_id,))
                room_name = cursor.fetchone()[0]

                # Open the chat window using open_chat function
                self.client = Client(self.username, self, room_name)
                self.room_name = room_name
                self._chat_window()
                self.join_window.destroy()
            else:
                messagebox.showwarning("Input Error", "Room ID does not exist!")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            cursor.close()
            connection.close()

    def join_chat_room(self):
        join_window = Toplevel(self.window)
        self.join_window = join_window
        join_window.title("Join Chat Room by ID")
        width = 350
        height = 200

        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()

        x = int((screenwidth / 2) - (width / 2))
        y = int((screenheight / 2) - (height / 2))
        join_window.geometry(f"{width}x{height}+{x}+{y}")

        Label(join_window, text="Enter Room ID:").pack(pady=10)
        room_id_entry = Entry(join_window)
        room_id_entry.pack(pady=10)

        def submit():
            room_id = room_id_entry.get()
            if room_id:
                self._join_chat_room_by_id(room_id)
                join_window.destroy()
            else:
                messagebox.showwarning("Input Error", "Room ID is required!")

        Button(join_window, text="Join", command=submit).pack(pady=20)
        Button(join_window, text="Cancel", command=join_window.destroy).pack(pady=10)
        
app = ChatWindow()
app.run()
sys.exit()  