#Interactive, CLI based implementation of Go Fish.
#See the README.MD for full rules.

import os
import time
import random

#The 13 possible face values. Each of these represents one Book.
VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Ace", "Jack", "King", "Queen"]

#Prints a message with a wait before continuing.
def say(msg):
    print(msg)
    time.sleep(1.5)

#Clears string. Used at start of game/turn.
def clear():
    os.system("clear||cls") #Platform indepent screen clearing

#Class for managing card.
class Card():
    def __init__(self, v, s):
        self.Value = v
        self.Suite = s
        
#Class that runs the game and manages it's variables.
class Game():

    #Function that runs the game and initializes variables.
    def __init__(self):
        clear()

        self.deck           = []
        self.playerHand     = []
        self.computerHand   = []
        self.playerBooks    = []
        self.computerBooks  = []
        self.turnCount      = 0      
        self.giveUp         = False
        self.turn           = random.choice([True, False]) #True for human turn, False for computer turn

        #Construct and shuffle Deck
        for i in VALUES:
            for j in ["Clubs", "Diamonds", "Hearts", "Spades"]:
                self.deck.append(Card(i, j))
        random.shuffle(self.deck)

        say("Beginning game!")
        say("Tossing coin to determine who goes first...")

        if self.turn:
            say("You go first! Each player now draws 7 cards...")
        else:
            say("The Computer goes first! Each player nows draw 7 cards...")

        for i in range(7): #Each player draws 7 cards
            self.playerDraw(show=False)
            self.computerDraw()

        say("Checking for Books in initial draws...")
        self.checkPlayerBooks()
        self.checkComputerBooks()
        input("Press enter to begin the game now.")

        while True:
            self.turnCount += 1
            if self.turn:
                self.playerTurn()
            else:
                self.computerTurn()
            #self.turn is modified in the playerTurn()/computerTurn() method
            
            #Having a majority of books (7), an empty hand, an empty deck, and forefitting end the game.
            if (len(self.playerBooks) > 6 or len(self.computerBooks) > 6
            or len(self.playerHand) == 0 or len(self.computerHand) == 0
            or len(self.deck) == 0 or self.giveUp):
                break

        clear()

        if self.giveUp:
            say("You have forefited the game. The computer wins!")
            say("Here are the final results.\n")

        else:
            if len(self.playerBooks) > 6 or len(self.computerBooks) > 6:
                say("Hold on! Someone has completed 7 Books.")
            elif len(self.playerHand) == 0 or len(self.computerHand) == 0:
                say("Hold on! Someone has an empty hand.")
            else:
                say("Hold on! The deck has been emptied.")

            say("That means the game is over. Here are the final results...\n")

            if len(self.playerBooks) > len(self.computerBooks):
                say("Congratulations, you are the winner!")
            elif len(self.playerBooks) < len(self.computerBooks):
                say("The Computer won! Better luck next time.")
            else:
                say("It's a draw! Neither player won.")

        print(f"\nGame results:\n"+
              f"Turn Count: {self.turnCount}\n"+
              f"Final deck size: {len(self.deck)}\n"+
              f"Your       Books ({len(self.playerBooks)}): {self.playerBooks}\n"+
              f"Computer's Books ({len(self.computerBooks)}): {self.computerBooks}\n\n")

        
        input("Press enter to clear this screen and return to the main menu.")
        clear()

    #Used to draw a card. When drawing 7 cards at the start, the message is omitted.
    def playerDraw(self, show=True):
        self.playerHand.append(self.deck.pop())
        if show:
            drawnCard = self.playerHand[-1]
            say(f"The card you just drew is a {drawnCard.Value} of {drawnCard.Suite}.")

    #Used to have the computer draw a card.
    def computerDraw(self):
        self.computerHand.append(self.deck.pop())

    #Checks if the player has a Book, and if so, remove it from their hand and add it to their books..
    def checkPlayerBooks(self):
        for i in VALUES:
            if sum(card.Value==i for card in self.playerHand) == 4:
                say(f"You have completed the Book for Value {i}!")
                say(f"You now discard all 4 cards of that Value.")
                self.playerHand = [card for card in self.playerHand if card.Value!=i]
                self.playerBooks.append(i)
                say(f"You have completed {len(self.playerBooks)} Books.")
                break #It is only possible to hold one Book at a time, so no need to keep looping

    #Same as checkPlayerBooks, but for the Computer. (Strings are different.)
    def checkComputerBooks(self):
        for i in VALUES:
            if sum(card.Value==i for card in self.computerHand) == 4:
                say(f"The computer has completed the Book for value {i}!")
                say(f"Computer now discards all 4 cards of that Value.")
                self.computerHand = [card for card in self.computerHand if card.Value!=i]
                self.computerBooks.append(i)
                say(f"The computer has completed {len(self.computerBooks)} Books.")
                break

    #Outputs a list of cards in the player's hand. Sorted by value, and includes a count of the number of cards of that value.
    def printHand(self):
        output = ""

        for i in VALUES:
            cards = [card for card in self.playerHand if card.Value==i]
            if len(cards) > 0:
                string = ""
                for s in cards:
                    string += f"{s.Suite}, "
                string = string[:-2] #Exlcude space and comma added after last element
                cardValue = i.ljust(5) #Left justifies Value field so they are all aligned
                output += f"{cardValue} ({len(cards)}): {string}\n"

        return output

    #Function used to transfer cards of the guessed type from one player to the other.
    #Takes in the current hands by value, and returns the updated hands.
    def surrender(self, givingHand, takingHand, value):
        takingHand = takingHand + [card for card in givingHand if card.Value==value]
        givingHand = [card for card in givingHand if card.Value!=value]
        return givingHand, takingHand

    #Function for running player turn.
    def playerTurn(self): 
        clear()

        print(
        f"Turn Count: {self.turnCount}, Deck Size: {len(self.deck)}\n"+
        f"Current Turn: Player\n"+
        f"Player has completed   {len(self.playerBooks)} Books and is holding {len(self.playerHand)} cards.\n"+
        f"Computer has completed {len(self.computerBooks)} Books and is holding {len(self.computerHand)} cards.\n"+
        f"You have the following cards in your hand:\n\n{self.printHand()}\n"+
        f"Enter the Value you would like to ask your opponent for.\n"+
        f"You must hold at least one card of such Value to do so.\n"+
        f"Enter \"Exit\" to forefit the game.\n(All input is case insensitive).\n"
        )

        guess = ""
        while not guess:
            guess = input()

            if guess.lower() == "exit":
                self.giveUp = True
                return

            if guess.lower() in ["jack", "king", "queen", "ace"]: #Allows case insensitive input
                guess = guess.lower().capitalize()

            if guess not in VALUES:
                print("ERROR: Input value not in accepted range. Enter an integer from 2-10,\n"+
                      "or one of the words Jack, King, Queen, Ace or Exit in any casing.\n")
                guess = ""
                continue

            if sum(card.Value==guess for card in self.playerHand) == 0:
                print("ERROR: You are not holding a card of the provided input value.\n")
                guess = ""
                continue

        say(f"Player asks the computer: got any {guess}s?")
        num = sum(card.Value==guess for card in self.computerHand)

        if num > 0:
            say(f"Computer has {num} cards with such value! Computer surrenders those cards to Player.")
            self.computerHand, self.playerHand = self.surrender(self.computerHand, self.playerHand, guess)
            say("Due to your correct guess, you get an extra turn!")
            
        else:
            self.turn = not self.turn
            say("Sorry, computer has no cards with such value.")
            say("Player, go fish! You draw a card.")
            self.playerDraw()
            
            if self.playerHand[-1].Value==guess:
                self.turn = not self.turn
                say(f"Congratulations! The card you just drew is of the value you guessed. You get an extra turn!")

        self.checkPlayerBooks()

        if self.turn:
            input("Press enter to close this text and start your extra turn.")
        else:
            input("Press enter to close this text and start the computer's turn.")

    #Function for running a computer's turn.
    def computerTurn(self):
        clear()

        print(
        f"Turn Count: {self.turnCount}, Deck Size: {len(self.deck)}\n"+
        f"Current Turn: Computer\n"+
        f"Player has completed   {len(self.playerBooks)} Books and is holding {len(self.playerHand)} cards.\n"+
        f"Computer has completed {len(self.computerBooks)} Books and is holding {len(self.computerHand)} cards.\n"+
        f"You have the following cards in your hand:\n\n{self.printHand()}\n")

        say("The computer is thinking of what to ask...")
        guess = random.choice(self.computerHand).Value #For now, its random.
        say(f"The computer asks you: got any {guess}s?")

        num = sum(card.Value==guess for card in self.playerHand)

        if num > 0:
            say(f"You are holding {num} cards with such Value! You surrender them to the Computer.")
            self.playerHand, self.computerHand = self.surrender(self.playerHand, self.computerHand, guess)
            say("Due to its correct guess, the computer gains an extra turn!")

        else:
            self.turn = not self.turn
            say("Nope, you have no cards with such Value.")
            say("The computer must Go Fish! Computer draws a card.")

            self.computerDraw()
            if self.computerHand[-1].Value==guess:
                self.turn = not self.turn
                say(f"The card the computer just drew is of their guessed value, {guess}. The computer gets an extra turn!")

        self.checkComputerBooks()

        if self.turn:
            input("Press enter to close this text and start your turn.")
        else:
            input("Press enter to close this text and start the computer's extra turn.")

def main():
    while True:
        result = input("Welcome to aelna354's Go Fish Game!\n"+
        "(Consult the README.MD file to view the rules.)\n"
        "Enter exit in any casing to close the program.\n"+
        "Otherwise, press enter to start the game.\n")
        
        if result.lower() != "exit":
            Game()
            continue

        break

main()