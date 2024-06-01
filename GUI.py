import customtkinter as ctk
from tkinter import messagebox
import requests
import random
import time

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

class FlashcardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Flashcard App")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")

        self.current_screen = LoginScreen(self)
        self.current_screen.pack(fill="both", expand=True)

        self.bind("<Escape>", self.exit_application)

    def exit_application(self, event=None):
        self.destroy()

    def switch_screen(self, new_screen, username=None, flashcard=None, stats=None):
        self.current_screen.destroy()
        if username and flashcard:
            self.current_screen = new_screen(self, username=username, flashcard=flashcard)
        elif username and stats:
            self.current_screen = new_screen(self, username=username, stats=stats)
        elif username:
            self.current_screen = new_screen(self, username=username)
        elif flashcard:
            self.current_screen = new_screen(self, flashcard=flashcard)
        else:
            self.current_screen = new_screen(self)
        self.current_screen.pack(fill="both", expand=True)

class MenuScreen(ctk.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username = username

        self.label = ctk.CTkLabel(self, text="Main Menu", font=("Helvetica", 24))
        self.label.place(relx=0.5, rely=0.1, anchor="center")

        self.logout_button = ctk.CTkButton(self, text="Logout", command=self.logout, width=120, height=40, corner_radius=10)
        self.logout_button.place(relx=0.9, rely=0.1, anchor="center")

        self.search_flashcards_button = ctk.CTkButton(self, text="Search Flashcards", command=self.show_flashcards, width=300, height=100, corner_radius=10)
        self.search_flashcards_button.place(relx=0.5, rely=0.3, anchor="center")

        self.create_flashcard_button = ctk.CTkButton(self, text="Create Flashcard", command=self.create_flashcard, width=300, height=100, corner_radius=10)
        self.create_flashcard_button.place(relx=0.5, rely=0.5, anchor="center")

        self.my_flashcards_button = ctk.CTkButton(self, text="My Flashcards", command=self.show_my_flashcards, width=300, height=100, corner_radius=10)
        self.my_flashcards_button.place(relx=0.5, rely=0.7, anchor="center")

    def logout(self):
        self.master.switch_screen(LoginScreen)

    def create_flashcard(self):
        self.master.switch_screen(CreateFlashcardScreen, username=self.username)

    def show_flashcards(self):
        self.master.switch_screen(SearchFlashcardsScreen, username=self.username)

    def show_my_flashcards(self):
        self.master.switch_screen(MyFlashcardsScreen, username=self.username)

class BaseManagemnetFlashcardScreen(ctk.CTkFrame):
    def __init__(self, master, username, title=""):
        super().__init__(master)
        self.master = master
        self.username = username

        self.label = ctk.CTkLabel(self, text=title, font=("Helvetica", 24))
        self.label.place(relx=0.5, rely=0.1, anchor="center")

        self.name_entry = ctk.CTkEntry(self, placeholder_text="name", width=300)
        self.name_entry.place(relx=0.5, rely=0.2, anchor="center")

        self.add_button = ctk.CTkButton(self, text="+", command=self.add_flashcard)
        self.add_button.place(relx=0.4, rely=0.3, anchor="center")

        self.remove_button = ctk.CTkButton(self, text="-", command=self.remove_flashcard)
        self.remove_button.place(relx=0.6, rely=0.3, anchor="center")

        self.save_button = ctk.CTkButton(self, text="Save flashcard", command=self.save_flashcards)
        self.save_button.place(relx=0.4, rely=0.9, anchor="center")

        self.back_button = ctk.CTkButton(self, text="Back to menu", command=self.back_to_menu)
        self.back_button.place(relx=0.6, rely=0.9, anchor="center")

        self.flashcard_frame = ctk.CTkScrollableFrame(self, width=500, height=50)
        self.flashcard_frame.place(relx=0.5, rely=0.6, anchor="center")

        self.flashcard_frames = []

    def add_flashcard(self):
        flashcard_frame = ctk.CTkFrame(self.flashcard_frame)
        flashcard_frame.pack(fill="x", pady=5)
        
        title_entry = ctk.CTkEntry(flashcard_frame, placeholder_text="1. word", width=250)
        title_entry.pack(side="left", padx=(5, 10))

        content_entry = ctk.CTkEntry(flashcard_frame, placeholder_text="2. word", width=250)
        content_entry.pack(side="left", padx=(0, 5))

        self.flashcard_frames.append((flashcard_frame, title_entry, content_entry))

    def remove_flashcard(self):
        if len(self.flashcard_frames) > 1:
            flashcard_frame, title_entry, content_entry = self.flashcard_frames.pop()
            flashcard_frame.destroy()

    def save_flashcards(self):
        pass

    def back_to_menu(self):
        self.master.switch_screen(MenuScreen, username=self.username)


class CreateFlashcardScreen(BaseManagemnetFlashcardScreen):
    def __init__(self, master, username):
        super().__init__(master, username, title="Create Flashcard")
        super().add_flashcard()

    def save_flashcards(self):
        flashcards_data = {}

        for _, title_entry, content_entry in self.flashcard_frames:
            title = title_entry.get()
            content = content_entry.get()
            if title and content:
                flashcards_data[title] = content

        title = self.name_entry.get()
        if flashcards_data and title:
            url = 'http://localhost:5000/flashcards/add'
            data = {
                'username': self.username,
                'content': flashcards_data,
                'title': title
            }
            response = requests.post(url, json=data)
            response_data = response.json()
            if response.status_code == 201:
                messagebox.showinfo("Success", response_data.get("message"))
                self.back_to_menu()
            else:
                messagebox.showerror("Error", response_data.get("message"))
        else:
            messagebox.showwarning("Error", "Fields are missing")


class EditFlashcardScreen(BaseManagemnetFlashcardScreen):
    def __init__(self, master, username, flashcard):
        super().__init__(master, username, title="Edit Flashcard")
        self.flashcard = flashcard
        self.load_content()
        self.name_entry.insert(0, flashcard.get("title"))

    def load_content(self):
        for key, value in self.flashcard.get("content", {}).items():
            flashcard_frame = ctk.CTkFrame(self.flashcard_frame)
            flashcard_frame.pack(fill="x", pady=5)

            title_entry = ctk.CTkEntry(flashcard_frame, placeholder_text="Flashcard title", width=250)
            title_entry.insert(0, key)
            title_entry.pack(side="left", padx=(5, 10))

            content_entry = ctk.CTkEntry(flashcard_frame, placeholder_text="Flashcard content", width=250)
            content_entry.insert(0, value)
            content_entry.pack(side="left", padx=(0, 5))

            self.flashcard_frames.append((flashcard_frame, title_entry, content_entry))

    def save_flashcards(self):
        flashcards_data = {}

        for _, title_entry, content_entry in self.flashcard_frames:
            title = title_entry.get()
            content = content_entry.get()
            if title and content:
                flashcards_data[title] = content

        title = self.name_entry.get()
        if flashcards_data and title:
            url = f'http://localhost:5000/flashcards/edit/{self.flashcard.get("id")}'
            data = {
                'content': flashcards_data,
                'title': title
            }
            response = requests.put(url, json=data)
            response_data = response.json()
            if response.status_code == 200:
                messagebox.showinfo("Success", response_data.get("message"))
                self.back_to_menu()
            else:
                messagebox.showerror("Error", response_data.get("message"))
        else:
            messagebox.showwarning("Error", "Fields are missing")

class BaseFlashcardsScreen(ctk.CTkFrame):
    def __init__(self, master, username, label_text=None):
        super().__init__(master)
        self.master = master
        self.username = username
        self.flashcards = []

        if label_text:
            self.label = ctk.CTkLabel(self, text=label_text, font=("Helvetica", 24))
            self.label.place(relx=0.5, rely=0.1, anchor="center")

        self.back_button = ctk.CTkButton(self, text="Back to menu", command=self.back_to_menu, width=200, height=50)
        self.back_button.place(relx=0.5, rely=0.95, anchor="center")

        self.flashcard_frame = ctk.CTkScrollableFrame(self, width=700, height=400)
        self.flashcard_frame.place(relx=0.5, rely=0.5, anchor="center")

    def clear_flashcards(self):
        for widget in self.flashcard_frame.winfo_children():
            widget.destroy()

    def load_flashcards(self, url, isMine=False):
        response = requests.get(url)
        if response.status_code == 200:
            flashcards_data = response.json()
            self.flashcards = flashcards_data
            self.show_flashcards(isMine=isMine)

    def show_flashcard_details(self, flashcard):
        self.master.switch_screen(DetailsFlashardScreen, flashcard=flashcard, username=self.username)

    def edit_flashcard(self, flashcard):
        self.master.switch_screen(EditFlashcardScreen, username=self.username, flashcard=flashcard)

    def show_flashcards(self, isMine):
        self.clear_flashcards()
        for i, flashcard in enumerate(self.flashcards):
                flashcard_button = ctk.CTkButton(
                    self.flashcard_frame,
                    text=flashcard['title'],
                    width=150,
                    height=150,
                    command=lambda f=flashcard: self.show_flashcard_details(f)
                )
                flashcard_button.grid(row=i // 4 * 2, column=i % 4, padx=10, pady=(10, 5))

                if isMine:
                    button_frame = ctk.CTkFrame(self.flashcard_frame)
                    button_frame.grid(row=i // 4 * 2 + 1, column=i % 4, padx=10, pady=(0, 10))

                    edit_button = ctk.CTkButton(
                        button_frame,
                        text="Edit",
                        width=60,
                        height=30,
                        command=lambda f=flashcard: self.edit_flashcard(f)
                    )
                    edit_button.pack(side="left", padx=(0, 5))

                    delete_button = ctk.CTkButton(
                        button_frame,
                        text="Delete",
                        width=60,
                        height=30,
                        command=lambda f=flashcard: self.delete_flashcard(f)
                    )
                    delete_button.pack(side="left", padx=(5, 0))

    def delete_flashcard(self, flashcard):
        confirm = messagebox.askyesno("Delete flashcard?", "Are you sure you want to delete this flashcard?")
        if confirm:
            _id = flashcard.get("id")
            url = f"http://localhost:5000/flashcards/delete/{_id}"
            response = requests.delete(url)
            response_data = response.json()
            if response.status_code == 200:
                messagebox.showinfo("Success", response_data.get("message"))
                self.flashcards = [data for data in self.flashcards if data["id"] != _id]
                self.show_flashcards(isMine=True)
            else:
                messagebox.showerror("Error", response_data.get("message"))

    def back_to_menu(self):
        self.master.switch_screen(MenuScreen, username=self.username)

class SearchFlashcardsScreen(BaseFlashcardsScreen):
    def __init__(self, master, username):
        super().__init__(master, username)
        
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Name", width=400)
        self.search_entry.place(relx=0.3, rely=0.1, anchor="center")

        self.search_button = ctk.CTkButton(self, text="Search", command=self.search, width=100, height=20)
        self.search_button.place(relx=0.65, rely=0.1, anchor="center")

        self.load_flashcards("http://localhost:5000/flashcards")
    
    def search(self):
        search_query = self.search_entry.get()
        if search_query:
            url = f"http://localhost:5000/flashcards/search/{search_query}"
            self.load_flashcards(url)
        else:
            self.load_flashcards("http://localhost:5000/flashcards")


class MyFlashcardsScreen(BaseFlashcardsScreen):
    def __init__(self, master, username):
        super().__init__(master, username, "My flashcards")
        self.load_flashcards(f"http://localhost:5000/flashcards/{self.username}", isMine=True)

class DetailsFlashardScreen(ctk.CTkFrame):
    def __init__(self, master, flashcard, username):
        super().__init__(master)
        self.master = master
        self.flashcard = flashcard
        self.current_index = 0
        self.username = username
        
        self.content = self.flashcard['content']
        self.passwords = list(self.content.keys())
        self.answers = list(self.content.values())
        
        self.flashcard_title = ctk.CTkLabel(self, text=flashcard['title'], font=("Helvetica", 18))
        self.flashcard_title.place(relx=0.5, rely=0.1, anchor="center")

        flashcard_button = ctk.CTkButton(self, text=self.passwords[self.current_index], width=150, height=150)
        flashcard_button.place(relx=0.5, rely=0.3, anchor="center")
        flashcard_button.configure(command=lambda: self.toggle_text(flashcard_button,self.passwords[self.current_index], self.answers[self.current_index]))

        self.left_arrow_button = ctk.CTkButton(self, text="←", command=self.scroll_left, width=50, height=50)
        self.left_arrow_button.place(relx=0.1, rely=0.3, anchor="center")

        self.right_arrow_button = ctk.CTkButton(self, text="→", command=self.scroll_right, width=50, height=50)
        self.right_arrow_button.place(relx=0.9, rely=0.3, anchor="center")

        self.check_knowledge_button = ctk.CTkButton(self, text="Check knowledge", command=self.check_knowledge, width=200, height=50)
        self.check_knowledge_button.place(relx=0.5, rely=0.75, anchor="center")

        self.memory_game_button = ctk.CTkButton(self, text="Memory game", command=self.memory_game, width=200, height=50)
        self.memory_game_button.place(relx=0.5, rely=0.85, anchor="center")
        
        self.back_button = ctk.CTkButton(self, text="Back", command=self.back, width=200, height=50)
        self.back_button.place(relx=0.5, rely=0.95, anchor="center")

    def check_knowledge(self):
        self.master.switch_screen(CheckKnowledgeScreen, username=self.username, flashcard=self.flashcard)

    def memory_game(self):
        self.master.switch_screen(MemoryGame, username=self.username, flashcard=self.content)

    def scroll_left(self):
        self.current_index -= 1
        if self.current_index < 0:
            self.current_index = len(self.passwords) - 1
        self.show_next()

    def scroll_right(self):
        self.current_index += 1
        if self.current_index >= len(self.passwords):
            self.current_index = 0
        self.show_next()

    def show_next(self):
        for widget in self.winfo_children():
            if widget not in [self.flashcard_title, self.left_arrow_button, self.right_arrow_button, self.back_button, self.check_knowledge_button, self.memory_game_button]:
                widget.destroy()
        flashcard_button = ctk.CTkButton(self, text=self.passwords[self.current_index], width=150, height=150)
        flashcard_button.place(relx=0.5, rely=0.3, anchor="center")
        flashcard_button.configure(command=lambda: self.toggle_text(flashcard_button, self.passwords[self.current_index], self.answers[self.current_index]))

    def toggle_text(self, button, password, answer):
        if button.cget("text") == password:
            button.configure(text=answer)
        else:
            button.configure(text=password)
    
    def back(self):
        if self.flashcard['username'] == self.username:
            self.master.switch_screen(MyFlashcardsScreen, username=self.username)
        else:
            self.master.switch_screen(SearchFlashcardsScreen, username=self.username)

class CheckKnowledgeScreen(ctk.CTkFrame):
    def __init__(self, master, username, flashcard):
        super().__init__(master)
        self.master = master
        self.username = username
        self.flashcard = flashcard
        self.content = flashcard.get("content")
        self.total = 0
        self.errors = 0
        self.correct = 0
        self.start = time.time()
        self.remaining_passwords = []

        self.back_button = ctk.CTkButton(self, text="Back", command=self.back, width=200, height=50)
        self.back_button.place(relx=0.5, rely=0.95, anchor="center")

        self.start_knowledge_check()

    def start_knowledge_check(self):
        if self.content:
            self.remaining_content = list(self.content.items())
            self.show_next_flashcard()
        else:
            self.back_to_menu()

    def check_answer(self, correct_answer):
        user_answer = self.answer_entry.get()
        self.total += 1
        if user_answer.lower() == correct_answer.lower():
            self.correct += 1
            self.show_next_flashcard()
        else:
            self.errors += 1
            self.show_next_flashcard()

    def show_next_flashcard(self):
        if self.remaining_content:
            next_flashcard = random.choice(self.remaining_content)
            self.remaining_content.remove(next_flashcard)

            for widget in self.winfo_children():
                if widget not in [self.back_button]:
                    widget.destroy()

            self.flashcard_label = ctk.CTkLabel(self, text=next_flashcard[0], font=("Helvetica", 24))
            self.flashcard_label.place(relx=0.5, rely=0.4, anchor="center")

            self.answer_entry = ctk.CTkEntry(self, placeholder_text="Answer:", width=300)
            self.answer_entry.place(relx=0.5, rely=0.5, anchor="center")

            self.submit_button = ctk.CTkButton(self, text="Next", command=lambda: self.check_answer(next_flashcard[1]))
            self.submit_button.place(relx=0.5, rely=0.6, anchor="center")
        else:
            duration = round(time.time() - self.start, 2)
            stats = {"total": self.total, "errors": self.errors, "correct": self.correct, "time": duration}
            self.master.switch_screen(CheckKnowledgeStatsScreen, username=self.username, stats=stats)

    def back(self):
        self.master.switch_screen(DetailsFlashardScreen, flashcard=self.flashcard, username=self.username)

class CheckKnowledgeStatsScreen(ctk.CTkFrame):
    def __init__(self, master, username, stats):
        super().__init__(master)
        self.master = master
        self.username = username
        self.stats = stats

        self.label = ctk.CTkLabel(self, text="Statistics", font=("Helvetica", 24))
        self.label.place(relx=0.5, rely=0.1, anchor="center")

        self.total_label = ctk.CTkLabel(self, text=f'Total cards: {self.stats.get("total")}', font=("Helvetica", 16))
        self.total_label.place(relx=0.5, rely=0.3, anchor="center")

        self.time_label = ctk.CTkLabel(self, text=f'Time: {self.calculate_time()}', font=("Helvetica", 16))
        self.time_label.place(relx=0.5, rely=0.4, anchor="center")

        self.correct_label = ctk.CTkLabel(self, text=f'Correct answers: {self.stats.get("correct")}', font=("Helvetica", 16))
        self.correct_label.place(relx=0.5, rely=0.5, anchor="center")

        self.incorrect_label = ctk.CTkLabel(self, text=f'Incorrect answers: {self.stats.get("errors")}', font=("Helvetica", 16))
        self.incorrect_label.place(relx=0.5, rely=0.6, anchor="center")

        self.accuracy_label = ctk.CTkLabel(self, text=f'Accuracy: {self.calculate_accuracy()}%', font=("Helvetica", 16))
        self.accuracy_label.place(relx=0.5, rely=0.7, anchor="center")

        self.back_button = ctk.CTkButton(self, text="Back to menu", command=self.back_to_menu)
        self.back_button.place(relx=0.5, rely=0.8, anchor="center")

    def calculate_accuracy(self):
        correct = self.stats.get('correct', 0)
        total = self.stats.get('total', 0)
        if total > 0:
            accuracy = (correct / total) * 100
            return round(accuracy, 2)
        return 0

    def calculate_time(self):
        seconds = int(self.stats.get("time"))
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        
        formatted_time = ""
        if hours > 0:
            formatted_time += f"{hours} h "
        if minutes > 0:
            formatted_time += f"{minutes} m "
        formatted_time += f"{seconds} s"
        
        return formatted_time

    def back_to_menu(self):
        self.master.switch_screen(MenuScreen, username=self.username)

class MemoryGame(ctk.CTkFrame):
    def __init__(self, master, username, flashcard):
        super().__init__(master)
        self.master = master
        self.username = username
        
        self.content = flashcard
        self.keys = list(self.content.keys())
        self.values = list(self.content.values())
        self.questions = self.keys + self.values
        
        self.flashcard_frame = ctk.CTkScrollableFrame(self, width=700, height=450)
        self.flashcard_frame.place(relx=0.5, rely=0.4, anchor="center")
        
        self.first_card = None
        self.second_card = None
        self.matched_pairs = 0
        
        self.create_board()

    def randomize_cards(self):
        size = len(self.questions)
        self.random_questions_arr = []
        for _ in range(size):
            index = random.randint(0, len(self.questions) - 1)
            element = self.questions.pop(index)
            self.random_questions_arr.append(element)

    def create_board(self):
        self.randomize_cards()
        self.card_buttons = []
        for i, value in enumerate(self.random_questions_arr):
            flashcard_button = ctk.CTkButton(
                self.flashcard_frame,
                text=value,
                width=150,
                height=150,
                command=lambda i=i, value=value: self.on_card_click(i, value)
            )
            flashcard_button.grid(row=i // 4 * 2, column=i % 4, padx=10, pady=(10, 5))
            self.card_buttons.append(flashcard_button)
    
    def on_card_click(self, index, value):
        if self.first_card is None:
            self.first_card = (index, value)
        elif self.second_card is None:
            self.second_card = (index, value)
            self.master.after(500, self.check_match)

    def check_match(self):
        first_index, first_value = self.first_card
        second_index, second_value = self.second_card
        
        if (first_value in self.content and self.content[first_value] == second_value) or (second_value in self.content and self.content[second_value] == first_value):
            self.card_buttons[first_index].configure(state="disabled")
            self.card_buttons[second_index].configure(state="disabled")
            self.matched_pairs += 1
        
        self.first_card = None
        self.second_card = None
        
        if self.matched_pairs == len(self.keys):
            self.show_victory_message()

    def show_victory_message(self):
        replay_button = ctk.CTkButton(self, text="Play again", command=self.replay)
        replay_button.place(relx=0.5, rely=0.85, anchor="center")

        back_button = ctk.CTkButton(self, text="Back to menu", command=self.back_to_menu)
        back_button.place(relx=0.5, rely=0.95, anchor="center")

    def replay(self):
        self.master.switch_screen(MemoryGame, username=self.username, flashcard=self.content)

    def back_to_menu(self):
        self.master.switch_screen(MenuScreen, username=self.username)

if __name__ == "__main__":
    app = FlashcardApp()
    app.mainloop()
