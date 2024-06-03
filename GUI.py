import customtkinter as ctk
from authorize import LoginScreen

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

    def switch_screen(self, new_screen, username=None, flashcard=None, stats=None, user=None):
        self.current_screen.destroy()
        if username and flashcard and user:
            self.current_screen = new_screen(self, username=username, flashcard=flashcard, user=user)
        elif username and flashcard:
            self.current_screen = new_screen(self, username=username, flashcard=flashcard)
        elif username and stats:
            self.current_screen = new_screen(self, username=username, stats=stats)
        elif username and user:
            self.current_screen = new_screen(self, username=username, user=user)
        elif username:
            self.current_screen = new_screen(self, username=username)
        elif flashcard:
            self.current_screen = new_screen(self, flashcard=flashcard)
        else:
            self.current_screen = new_screen(self)
        self.current_screen.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = FlashcardApp()
    app.mainloop()
