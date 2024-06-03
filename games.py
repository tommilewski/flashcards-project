import customtkinter as ctk
import random
import time

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
        from flashcards import DetailsFlashardScreen
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
        from menu import MenuScreen
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
        from menu import MenuScreen
        self.master.switch_screen(MenuScreen, username=self.username)