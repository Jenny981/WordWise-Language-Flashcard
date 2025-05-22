from datetime import datetime
import random
import os
class FlashcardManager:
    def __init__(self, words_file="words.txt", stats_file="stats.txt"):
        self.words_file = words_file
        self.stats_file = stats_file
        self.words = {}#dictionary to store words and their meanings
        self.stats = {
            "total_questions": 0,
            "correct_answers": 0,
            "accuracy": 0.0,
            "daily_words": {},  #record the words learned each day
            "streak": 0,  #continuous learning days
            "last_learned": None  #last learning date
        }
        self._ensure_data_dir_exists()
        self.load_words()

    def load_words(self):
        words = []
        try:
            with open(self.words_file, "r") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 2:
                        word, meaning = parts
                        self.words[word] = meaning
        except FileNotFoundError:
            print(f"Warning: {self.words_file} not found. Starting with empty word list.")

    def save_words(self):
        #save the words to the file
        try:
            with open(self.words_file, "w") as f:
                for word, meaning in self.words.items():
                    f.write(f"{word}|{meaning}\n")
        except Exception as e:
            print(f"Error saving words: {e}")
        #save the stats to the file
        try:
            with open(self.stats_file, "w") as f:
                f.write(f"total_questions={self.stats['total_questions']}\n")
                f.write(f"correct_answers={self.stats['correct_answers']}\n")
                f.write(f"accuracy={self.stats['accuracy']}\n")
                f.write(f"streak={self.stats['streak']}\n")
                f.write(f"last_learned={self.stats['last_learned'] or 'None'}\n")  
                #save daily words
                for date, words in self.stats["daily_words"].items():
                    f.write(f"{date}:{','.join(words)}\n")
        except Exception as e:
            print(f"Error saving stats: {e}")

    def _ensure_data_dir_exists(self):
        #create the data directory if it doesn't exist
        data_dir = os.path.dirname(self.words_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def add_word(self, word, meaning):
        #add a new word to the word list
        if word.lower() in self.words:
            print(f"Warning: {word} already exists.")
            return
        self.words[word.lower()] = meaning
        self.save_words()
        print(f"Added {word} to the word list.")
        
    def remove_word(self, word):
        #remove a word from the word list
        if word.lower() in self.words:
            del self.words[word.lower()]
            self.save_words()
            print(f"Removed {word} from the word list.")
        else:
            print(f"Warning: {word} not found in the word list.")

    def view_all_words(self):
        #view all words in the word list
        if not self.words:
            print("No words in the word list.")
            return
        print("===words list===")
        print(f'total words: {len(self.words)}')
        for i, (word, meaning) in enumerate(self.words.items(), 1):
            print(f"{i}. {word}: {meaning}")
        print("================")
        return
    
    def get_today_date(self):
        #get the current date
        return datetime.now().strftime("%d-%m-%Y")
    
    def update_streak(self):
        today = self.get_today_date()
        if self.stats["last_learned"] == today:
            self.stats["streak"] += 1
        else:
            self.stats["streak"] = 1
        self.stats["last_learned"] = today
        self.save_stats()
        
    def learn_daily_word(self):
        """
    Practice a random word from the word list as the daily word.
    Check if the user has already practiced today's words.
    Update the learning statistics and save them to the file.
        """
        #practice the words
        #get today's date
        today = self.get_today_date()
        #if no words, print a message and return
        if not self.words:
            print("You haven't added any words yet.")
            return  
        #check whether had practiced today
        if today in self.stats["daily_words"]:
            print("You've already practiced today's words.")
            return
        #get a random word from the word list as the daily  word
        random_word = random.choice(list(self.words.keys()))
        #print the word and its meaning
        print(f"Word: {random_word}")
        print(f"Meaning: {self.words[random_word]}")
        #get user input
        user_input = input("Enter the meaning of the word: ").lower()
        #check if the user input is correct
        if user_input == self.words[random_word].lower():
            print("Correct! You've earned a point.")
            self.stats["correct_answers"] += 1
        else:
            print(f"Incorrect. The correct meaning is '{self.words[random_word]}'.")
        self.stats["total_questions"] += 1
        self.update_streak()
        self.stats["accuracy"] = self.stats["correct_answers"] / self.stats["total_questions"]
        self.save_stats()

    def save_stats(self):
        #save the stats to the file
        try:
            with open(self.stats_file, "w") as f:
                f.write(f"total_questions: {self.stats['total_questions']}\n")
                f.write(f"correct_answers: {self.stats['correct_answers']}\n")
                f.write(f"accuracy: {self.stats['accuracy']}\n")
                f.write(f"streak: {self.stats['streak']}\n")
                f.write(f"last_learned: {self.stats['last_learned'] or 'None'}\n")
        except Exception as e:
            print(f"Error saving stats: {e}")

    def view_stats(self):
        print("=== Your Statistics ===")
        print(f"Total Questions: {self.stats['total_questions']}")
        print(f"Correct Answers: {self.stats['correct_answers']}")
        print(f"Accuracy: {self.stats['accuracy']:.2%}")
        print(f"Streak: {self.stats['streak']}")
        print(f"Last Learned Date: {self.stats['last_learned']}")
        print("=======================")

        
