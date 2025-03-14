import os
import time
from random_word import RandomWords
from users import update_score

class Game:
    """
    ---
    """
    def __init__(self, username=None):
        self._username = username 
        self.drawing = [
            r''' 
            +---+
            |   |
                |
                |
                |
                |
            =========''',
            r''' 
            +---+
            |   |
            O   |
                |
                |
                |
            =========''',
            r''' 
            +---+
            |   |
            O   |
            |   |
                |
                |
            =========''',
            r''' 
             +---+
             |   |
             O   |
            /|   |
                 |
                 |
            =========''',
            r''' 
             +---+
             |   |
             O   |
            /|\  |
                 |
                 |
            =========''',
            r''' 
             +---+
             |   |
             O   |
            /|\  |
            /    |
                 |
            =========''',
            r''' 
             +---+
             |   |
             O   |
            /|\  |
            / \  |
                 |
            ========='''
        ]
        self._word:str = RandomWords().get_random_word()
        self._guess:str = ""
        self._word_length:int= len(self._word)
        self._max_wrong_guesses:int = len(self.drawing)
        self._wrong_guesses:int = 0 
        self._correct_guesses:int = 0 
        self._wins:int = 0 
        self._used_letters:list = []
        self._correct_letters:list = []
        self._run:bool = True 
        self._playAgain:bool = False

    def validate_letter(self, letter):
        if letter in self._used_letters:
            print("pismeno uz bylo pouzito!")
            time.sleep(1.5)
            return False
        if len(letter) != 1 or not letter.isalpha():
            print("prosim zadejte jen jedno pismeno!")
            time.sleep(1.5)
            return False
        if self._wrong_guesses >= len(self.drawing) - 1:
            return False
        return True

    @property
    def correct_letters(self):
        return self._correct_letters

    @property
    def guess(self):
        return self._guess

    @property
    def max_wrong_guesses(self):
        return self._max_wrong_guesses

    @property
    def playAgain(self):
        return self._playAgain

    @property
    def wins(self):
        return self._wins

    @property
    def correct_guesses(self):
        return self._correct_guesses

    @property
    def used_letters(self):
        return self._used_letters

    @property
    def word(self):
        return self._word

    @property
    def word_length(self):
        return self._word_length

    @property
    def wrong_guesses(self):
        return self._wrong_guesses

    @property
    def run(self):
        return self._run

    def checkStatus(self):
        if self._wrong_guesses >= len(self.drawing) - 1:
            print(f"Prohrál jsi! Slovo bylo: {self._word}")
            return False
        elif self._correct_guesses >= len(self._word):
            self._wins += 1
            print(f"Vyhrál jsi! Slovo bylo: {self._word}")
            update_score(self._username, 1)  
            return False
        return True

    def display_word_progress(self):
        progress = "".join([letter if letter in self._correct_letters else "_" for letter in self._word])
        print(f"Slovo: {progress}")

    def start_game(self):
        os.system('cls' if os.name == 'nt' else 'clear')        
        while self._run:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"slovo co hadate ma {self._word_length} pismen")
            print(f"slovo je: {self.word}")
            print("pouzita pismena:", self.used_letters)
            print("spravna pismena:", self.correct_letters)
            current_wrong = min(self.wrong_guesses, len(self.drawing) - 1)
            print(self.drawing[current_wrong])
            self.display_word_progress()

            if not self.checkStatus():
                while True:
                    play_again = input("chcete hrat znova (ano/ne): ").lower()
                    if play_again == "ano":
                        self.__init__(self._username)
                        break
                    elif play_again == "ne":
                        self._run = False
                        break
                    else:
                        print("Pouze ano/ne")
                continue

            self._guess = input("napiste pismeno: ").lower()
            if self.validate_letter(self._guess):
                self._used_letters.append(self._guess)
                if self._guess in self._word:
                    self._correct_letters.append(self._guess)
                    self._correct_guesses += self._word.count(self._guess)
                    print(f"pismeno '{self._guess}' je spravne")
                else:
                    self._wrong_guesses += 1
                    print(f"spatne pismeno '{self._guess}' neni ve slove")
                time.sleep(1.5)
            

def game(username):
    g = Game(username=username)
    g.start_game()
    return g.wins

def main():
    username = os.getenv("USERNAME")
    if not username:
        print("No username provided. Exiting game.")
        return
    final_score = game(username)
    update_score(username, final_score)
    print("Game finished.")

if __name__ == '__main__':
    main()
