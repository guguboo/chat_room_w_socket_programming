from tkinter import *
from client import Client
import mysql.connector

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


class ChatWindow:
    def __init__(self):
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
        user_label = Label(self.changeableWindow, text="Username", font=FONT_BOLD, anchor='w', bg=BG_COLOR)
        user_label.place(relx=0.02, relwidth=0.4)
        self.user_box = Entry(self.changeableWindow, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.user_box.place(relx=0.02, rely=0.05, relheight=0.06, relwidth=0.3)
        self.user_box.bind("<Return>", self.on_enter_username)

        # Password
        pass_label = Label(self.changeableWindow, text="Password", font=FONT_BOLD, anchor='w', bg=BG_COLOR)
        pass_label.place(relx=0.02, rely=0.13, relwidth=0.4)
        self.pass_box = Entry(self.changeableWindow, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, show = "*")
        self.pass_box.place(relx=0.02, rely=0.18, relheight=0.06, relwidth=0.3)
        self.pass_box.bind("<Return>", self.on_enter_username)

        # OK
        send_button = Button(self.changeableWindow, text="OK", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self.on_enter_username(None))
        send_button.place(relx=0.34, rely=0.27, relheight=0.06, relwidth=0.1)

        # Register
        register_button = Button(self.changeableWindow, text="Register", font=FONT_BOLD, width=20, bg=BG_GRAY,
                                 command=self._register_window)
        register_button.place(relx=0.45, rely=0.27, relheight=0.06, relwidth=0.15)

        self.user_box.focus()

    def on_enter_username(self, event):
        self.username = self.user_box.get()
        self.password = self.pass_box.get()
        authenticated = self._authenticate_user()

        err_label = Label(self.changeableWindow, font=FONT, fg="red", bg=BG_COLOR, anchor='w')
        err_label.place(relx=0.02, rely=0.1, relwidth=0.5)
        if not authenticated:
            err_label.config(text="Username atau Password Salah")
        else:
            self.client = Client(self.username, self)
            self._chat_window()

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

                if user:
                    return True
                else:
                    return False

    def _register_window(self):
        self.clear_all()

        self.head_label.config(text="Register New User")

        # Username
        user_label = Label(self.changeableWindow, text="Username", font=FONT_BOLD, anchor='w', bg=BG_COLOR)
        user_label.place(relx=0.02, relwidth=0.4, rely=0.02)
        self.reg_user_box = Entry(self.changeableWindow, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.reg_user_box.place(relx=0.02, rely=0.07, relheight=0.06, relwidth=0.3)
        self.reg_user_box.bind("<Return>", self.on_register_user)

        # Password
        pass_label = Label(self.changeableWindow, text="Password", font=FONT_BOLD, anchor='w', bg=BG_COLOR)
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
        self.head_label.config(text="Chat Room V1 - Vico, Andrea, Nirvana")
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, pady=5, padx=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.960)
        scrollbar.configure(command=self.text_widget.yview)

        #btm label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        #buat ketik
        self.msg_box = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_box.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_box.focus()
        self.msg_box.bind("<Return>", self.on_enter_msg)

        #send btn
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self.on_enter_msg(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    def on_enter_msg(self, event):
        msg = self.msg_box.get()
        self.client.send_message(msg)
        return msg

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


app = ChatWindow()
app.run()