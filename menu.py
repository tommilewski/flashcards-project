import customtkinter as ctk
from flashcards import MyFlashcardsScreen, SearchFlashcardsScreen, CreateFlashcardScreen

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
        from authorize import LoginScreen
        self.master.switch_screen(LoginScreen)

    def create_flashcard(self):
        self.master.switch_screen(CreateFlashcardScreen, username=self.username)

    def show_flashcards(self):
        self.master.switch_screen(SearchFlashcardsScreen, username=self.username)

    def show_my_flashcards(self):
        self.master.switch_screen(MyFlashcardsScreen, username=self.username)