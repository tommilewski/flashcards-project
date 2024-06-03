import customtkinter as ctk
from tkinter import messagebox
import requests

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.label = ctk.CTkLabel(self, text="Login", font=("Helvetica", 24))
        self.label.place(relx=0.5, rely=0.1, anchor="center")

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username:", width=300)
        self.username_entry.place(relx=0.5, rely=0.3, anchor="center")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password:", width=300, show="*")
        self.password_entry.place(relx=0.5, rely=0.4, anchor="center")

        self.login_button = ctk.CTkButton(self, text="Log In", command=self.login)
        self.login_button.place(relx=0.5, rely=0.6, anchor="center")

        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.place(relx=0.5, rely=0.7, anchor="center")

    def login(self):
        from menu import MenuScreen
        username = self.username_entry.get()
        password = self.password_entry.get()

        url = "http://localhost:5000/login"
        data = {
            "username": username,
            "password": password
        }

        response = requests.post(url, json=data)
        response_data = response.json()
        if response.status_code == 200:
            self.master.switch_screen(MenuScreen, username=username)
        else:
            messagebox.showerror("Error", response_data.get("message"))

    def register(self):
        self.master.switch_screen(RegisterScreen)

class RegisterScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.label = ctk.CTkLabel(self, text="Register", font=("Helvetica", 24))
        self.label.place(relx=0.5, rely=0.1, anchor="center")

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username:", width=300)
        self.username_entry.place(relx=0.5, rely=0.3, anchor="center")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password:", width=300, show="*")
        self.password_entry.place(relx=0.5, rely=0.4, anchor="center")

        self.confirm_password_entry = ctk.CTkEntry(self, placeholder_text="Confirm Password:", width=300, show="*")
        self.confirm_password_entry.place(relx=0.5, rely=0.5, anchor="center")

        self.register_button = ctk.CTkButton(self, text="Register", command=self.register)
        self.register_button.place(relx=0.5, rely=0.6, anchor="center")

        self.back_button = ctk.CTkButton(self, text="Back to Login", command=self.back_to_login)
        self.back_button.place(relx=0.5, rely=0.7, anchor="center")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not all([username, password, confirm_password]):
            messagebox.showerror("Registration Error", "All fields are required")
        elif password != confirm_password:
            messagebox.showerror("Registration Error", "Passwords do not match")
        else:
            url = "http://localhost:5000/register"
            data = {
                "username": username,
                "password": password,
            }
            response = requests.post(url, json=data)
            response_data = response.json()
            if response.status_code == 200:
                messagebox.showinfo("Success", response_data.get("message"))
                self.back_to_login()
            else:
                messagebox.showerror("Error", response_data.get("message"))

    def back_to_login(self):
        self.master.switch_screen(LoginScreen)