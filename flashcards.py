import customtkinter as ctk
from tkinter import messagebox
import requests

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
        from menu import MenuScreen
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
    def __init__(self, master, username, label_text=None, user=None):
        super().__init__(master)
        self.master = master
        self.username = username
        self.flashcards = []
        self.user = user

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
        self.master.switch_screen(DetailsFlashardScreen, flashcard=flashcard, username=self.username, user=self.user)

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
        from menu import MenuScreen
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

class UserFlashcardsScreen(BaseFlashcardsScreen):
    def __init__(self, master, username, user):
        super().__init__(master, username, f"{user} flashcards", user)
        self.load_flashcards(f"http://localhost:5000/flashcards/{user}")

class DetailsFlashardScreen(ctk.CTkFrame):
    def __init__(self, master, flashcard, username, user=None):
        super().__init__(master)
        self.master = master
        self.flashcard = flashcard
        self.current_index = 0
        self.username = username
        self.user = user
        
        self.content = self.flashcard['content']
        self.passwords = list(self.content.keys())
        self.answers = list(self.content.values())
        
        self.flashcard_title = ctk.CTkLabel(self, text=f"name: {flashcard['title']}", font=("Helvetica", 18))
        self.flashcard_title.place(relx=0.5, rely=0.1, anchor="center")

        flashcard_button = ctk.CTkButton(self, text=self.passwords[self.current_index], width=150, height=150)
        flashcard_button.place(relx=0.5, rely=0.3, anchor="center")
        flashcard_button.configure(command=lambda: self.toggle_text(flashcard_button,self.passwords[self.current_index], self.answers[self.current_index]))

        self.left_arrow_button = ctk.CTkButton(self, text="←", command=self.scroll_left, width=50, height=50)
        self.left_arrow_button.place(relx=0.1, rely=0.3, anchor="center")

        self.right_arrow_button = ctk.CTkButton(self, text="→", command=self.scroll_right, width=50, height=50)
        self.right_arrow_button.place(relx=0.9, rely=0.3, anchor="center")

        self.username_label = ctk.CTkLabel(self, text=f"Flashcard created by: ", font=("Helvetica", 12))
        self.username_label.place(relx=0.4, rely=0.55, anchor="center")

        self.username_button = ctk.CTkButton(self, text=self.flashcard['username'], command=self.user_flashcards, width=100, height=50)
        self.username_button.place(relx=0.6, rely=0.55, anchor="center")

        self.check_knowledge_button = ctk.CTkButton(self, text="Check knowledge", command=self.check_knowledge, width=200, height=50)
        self.check_knowledge_button.place(relx=0.5, rely=0.75, anchor="center")

        self.memory_game_button = ctk.CTkButton(self, text="Memory game", command=self.memory_game, width=200, height=50)
        self.memory_game_button.place(relx=0.5, rely=0.85, anchor="center")
        
        self.back_button = ctk.CTkButton(self, text="Back", command=self.back, width=200, height=50)
        self.back_button.place(relx=0.5, rely=0.95, anchor="center")

    def check_knowledge(self):
        from games import CheckKnowledgeScreen
        self.master.switch_screen(CheckKnowledgeScreen, username=self.username, flashcard=self.flashcard)

    def memory_game(self):
        from games import MemoryGame
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
            if widget not in [self.flashcard_title, self.left_arrow_button, self.right_arrow_button, self.back_button, self.check_knowledge_button, self.memory_game_button, self.username_button, self.username_label]:
                widget.destroy()
        flashcard_button = ctk.CTkButton(self, text=self.passwords[self.current_index], width=150, height=150)
        flashcard_button.place(relx=0.5, rely=0.3, anchor="center")
        flashcard_button.configure(command=lambda: self.toggle_text(flashcard_button, self.passwords[self.current_index], self.answers[self.current_index]))

    def toggle_text(self, button, password, answer):
        if button.cget("text") == password:
            button.configure(text=answer)
        else:
            button.configure(text=password)

    def user_flashcards(self):

        if self.flashcard['username'] == self.username:
            self.master.switch_screen(MyFlashcardsScreen, username=self.username)
        else:
            self.master.switch_screen(UserFlashcardsScreen, username=self.username, user=self.flashcard['username'])

    def back(self):
        if self.flashcard['username'] == self.username:
            self.master.switch_screen(MyFlashcardsScreen, username=self.username)
        elif self.flashcard['username'] == self.user:
            self.master.switch_screen(UserFlashcardsScreen, username=self.username, user=self.user)
        else:
            self.master.switch_screen(SearchFlashcardsScreen, username=self.username)