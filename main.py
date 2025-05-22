from flashcard import FlashcardManager

def main():
    flashcard_manager = FlashcardManager()
    print("Welcome to WordWise - Flashcard Application")
    print('==========================================')

    while True:
        print("\nMain Menu")
        print('1.study daily word')
        print('2.add new word')
        print('3.view all words')
        print('4.delete word')
        print('5.check your stats')
        print('6.exit')

        try:
            choice = int(input("\nEnter your choice (1-6): "))
        except ValueError:
            print("Please enter a valid number!")
            continue

        if choice == 1:
            flashcard_manager.learn_daily_word()

        elif choice == 2:
            word = input("Enter the new English word: ").strip()
            if not word:
                print("Word cannot be empty!")
                continue
            meaning = input("Enter the meaning of the word: ").strip()
            if not meaning:
                print("Meaning cannot be empty!")
                continue
            if flashcard_manager.add_word(word, meaning):
                print(f"Successfully added word: {word} - {meaning}")

        elif choice == 3:
            flashcard_manager.view_all_words()

        elif choice == 4:
            word = input("Enter the word to delete: ").strip()  
            if word:
                if flashcard_manager.remove_word(word):
                    print(f"Successfully deleted word: {word}")
            else:
                print("Word cannot be empty!")
        
        elif choice == 5:
            flashcard_manager.view_stats()

        elif choice == 6:
            print("Thank you for using WordWise! Bye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()          
                
            


