from tkinter import *
import time
import random

#The 13 possible face values. Each of these represents one Book.
VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Ace", "Jack", "King", "Queen"]

class Card():
    def __init__(self, v, s):
        self.Value = v
        self.Suite = s

class GoFish():
    #clears screen
    def clear(self):
        self.terminal.config(state=NORMAL)
        self.terminal.delete(1.0, END)
        self.terminal.config(state=DISABLED)

    #Adds a string to the backlog
    def say(self, msg):
        self.messages.append(msg)

    #Prints out the log one at a time
    #Function behaves at little bit differently when called with playerTurn. Action parameter being true specifies that.
    def communicate(self, action=False):
        self.togglestart()

        timer = 0
        for i in self.messages[:-1]:
            self.master.after(timer, lambda i=i: self.printout(i))
            timer += 1500
        self.master.after(timer, lambda i=self.messages[-1]: self.printout(i, True)) #the last message has a true parameter so we can re-enable start button

        if action: #Highlight the cards after the last message is out if it is the player's turn
            self.master.after(timer, self.highlightCards)

        self.messages = [] #Clear the log of messages

    def highlightCards(self):
        for i in list(set(self.playerHand)): #unique values
            self.buttons[i.Value]['state'] = NORMAL
        self.togglestart()

    def printout(self, msg, last=False):
        self.terminal.config(state=NORMAL)
        self.terminal.insert(END, f"{msg}\n")
        self.terminal.config(state=DISABLED)

        if last:
            self.togglestart()

    def togglestart(self):
        if self.startbutton['state'] == 'disabled':
            self.startbutton['state'] = NORMAL
        else:
            self.startbutton['state'] = DISABLED

    def computerDraw(self):
        self.computerHand.append(self.deck.pop())

    def playerDraw(self, show=True):
        self.playerHand.append(self.deck.pop())
        if show:
            drawnCard = self.playerHand[-1]
            self.say(f"The card you just drew is a {drawnCard.Value} of {drawnCard.Suite}.")

    def status(self):
        self.clear()

        for i in VALUES:
            amount = sum(card.Value==i for card in self.playerHand)
            self.buttons[i]['text'] = f"{i} ({amount})"

        status= f"Turn Count: {self.turnCount}\n"

        if self.turn:
            status += "Current turn: Player\n"
        else:
            status += "Current turn: Computer\n"

        status += f"Deck size: {len(self.deck)}\n"
        status += f"Player is holding   {len(self.playerHand)} cards.\n"
        status += f"Computer is holding {len(self.computerHand)} cards.\n"
        status += f"Player has completed         {len(self.playerBooks)} Books.\n"
        status += f"Computer has completed       {len(self.computerBooks)} Books.\n"
        self.say(status)
    
    def surrender(self, givingHand, takingHand, value):
        takingHand = takingHand + [card for card in givingHand if card.Value==value]
        givingHand = [card for card in givingHand if card.Value!=value]
        return givingHand, takingHand

    def checkPlayerBooks(self):
        for i in VALUES:
            if sum(card.Value==i for card in self.playerHand) == 4:
                self.say(f"You have completed the Book for Value {i}!")
                self.playerHand = [card for card in self.playerHand if card.Value!=i]
                self.say(f"Cards of Value {i} discarded.")
                self.playerBooks.append(i)
                self.say(f"You have completed {len(self.playerBooks)} Books.")
                break

    def checkComputerBooks(self):
        for i in VALUES:
            if sum(card.Value==i for card in self.computerHand) == 4:
                self.say(f"The computer has completed the Book for Value {i}!")
                self.computerHand = [card for card in self.playerHand if card.Value!=i]
                self.say(f"Cards of Value {i} discarded.")
                self.computerBooks.append(i)
                self.say(f"The computer has completed {len(self.computerBooks)} Books.")
                break
    
    def computerTurn(self):
        self.status()
        self.say("The computer is thinking of what to ask...")
        guess = random.choice(self.computerHand).Value #For now, its random.
        self.say(f"The computer asks you: got any {guess}s?")

        num = sum(card.Value==guess for card in self.playerHand)

        if num > 0:
            self.say(f"You are holding {num} cards with such Value! You surrender them to the Computer.")
            self.playerHand, self.computerHand = self.surrender(self.playerHand, self.computerHand, guess)
            self.say("Due to its correct guess, the computer gains an extra turn!")

        else:
            self.turn = not self.turn
            self.say("Nope, you have no cards with such Value.")
            self.say("The computer must Go Fish! Computer draws a card.")

            self.computerDraw()
            if self.computerHand[-1].Value==guess:
                self.turn = not self.turn
                self.say(f"The card the computer just drew is of their guessed value, {guess}. The computer gets an extra turn!")

        self.checkComputerBooks()

        if self.turn:
            self.say("Press Start Turn to start your turn.")
        else:
            self.say("Press Start Turn to start the computer's extra turn.")

        self.communicate()

    def playerTurn(self):
        self.status()
        self.say("Select the Value of a card you hold at least one of,")
        self.say("to ask the computer if they have any cards of that value.")
        self.togglestart()
        self.communicate(action=True)

    def playerTurnPrime(self, val):
 
        #deactivate buttons
        for i in list(set(self.playerHand)):
            self.buttons[i.Value]['state'] = DISABLED

        self.say(f"Player asks the computer: got any {val}s?")
        num = sum(card.Value==val for card in self.computerHand)

        if num > 0:
            self.say(f"Computer has {num} cards of that value! Surrendering those cards to the Player.")
            self.computerHand, self.playerHand = self.surrender(self.computerHand, self.playerHand, val)
            self.say("Due to your correct guess, you get an extra turn!")
        else:
            self.turn = not self.turn
            self.say("Sorry, computer has no cards with such value.")
            self.say("Player, go fish! You draw a card.")
            self.playerDraw()

            if self.playerHand[-1].Value==val:
                self.turn = not self.turn
                self.say(f"Congratulations! The card you just drew is of the value you guessed. You get an extra turn!")

        self.checkPlayerBooks()
        
        if self.turn:
            self.say("Press the start button to start your extra turn.")
        else:
            self.say("Press the start button to start the computer's turn.")

        self.communicate()

    def startbutton(self):

        if not self.started: #Start the game
            self.started = True
            self.startbutton.config(text="Start Turn")
            self.clear()

            self.say("Beginning game!")
            self.say("Tossing a coin to determine who goes first...")
            if self.turn:
                self.say("You go first! Each player now draws 7 cards...")
            else:
                self.say("The computer goes first! Each player now draws 7 cards...")

            for i in range(7):
                self.playerDraw(show=False)
                self.computerDraw()

            self.say("Checking for Books in initial draws...")
            self.checkPlayerBooks()
            self.checkComputerBooks()
            self.say("Press Start Turn to begin the game.")
            self.communicate()

        else:
            self.turnCount += 1
            if self.turn:
                self.playerTurn()
            else:
                self.computerTurn()

            if (len(self.playerBooks) > 6 or len(self.computerBooks) > 6
            or len(self.playerHand) == 0 or len(self.computerHand) == 0
            or len(self.deck) == 0 or self.giveUp):
                self.endGame()

    def endGame(self):
        self.clear()

        if self.giveUp:
            self.say("You have forefited the game. The computer wins!")
            self.say("Here are the final results.\n")

        else:
            if len(self.playerBooks) > 6 or len(self.computerBooks) > 6:
                self.say("Hold on! Someone has completed 7 Books.")
            elif len(self.playerHand) == 0 or len(self.computerHand) == 0:
                self.say("Hold on! Someone has an empty hand.")
            else:
                self.say("Hold on! The deck has been emptied.")

            self.say("That means the game is over. Here are the final results...\n")

            if len(self.playerBooks) > len(self.computerBooks):
                self.say("Congratulations, you are the winner!")
            elif len(self.playerBooks) < len(self.computerBooks):
                self.say("The Computer won! Better luck next time.")
            else:
                self.say("It's a draw! Neither player won.")

        self.say(f"\nGame results:\n"+
              f"Turn Count: {self.turnCount}\n"+
              f"Final deck size: {len(self.deck)}\n"+
              f"Your       Books ({len(self.playerBooks)}): {self.playerBooks}\n"+
              f"Computer's Books ({len(self.computerBooks)}): {self.computerBooks}\n\n")

        self.communicate()

    def __init__(self, master):
        self.master = master
        self.messages = []
        self.started = False

        #SET UP GUI
        self.terminal = Text(self.master, height=20, width=80)
        self.terminal.grid(row=0, column=1)

        Button(self.master, width=8, text="Surrender", bg="yellow", fg="black", state=DISABLED).grid(row=3, column=0)
        self.startbutton = Button(self.master, width=8, command=self.startbutton, text="Start Game",
        bg='green', fg='white', disabledforeground='silver')
        self.startbutton.grid(row=3, column=2)

        self.buttons = {}

        buttons1 = Frame(self.master)
        for counter, value in enumerate(["Ace", "2", "3", "4", "5", "6", "7"]):
            self.buttons[value] = Button(buttons1, command=lambda i=value: self.playerTurnPrime(i), state=DISABLED, width=8, text=f"{value} (0)")
            self.buttons[value].grid(row=0, column=counter, padx=8)
        buttons1.grid(row=1, column=0, columnspan=7)

        buttons2 = Frame(self.master)
        for counter, value in enumerate(["8", "9", "10", "Jack", "King", "Queen"]):
            self.buttons[value] = Button(buttons2, command=lambda i=value: self.playerTurnPrime(i), state=DISABLED, width=8, text=f"{value} (0)")
            self.buttons[value].grid(row=0, column=counter, padx=8)
        buttons2.grid(row=2, column=0, columnspan=6)

        #BEGIN GAME
        self.deck           = []
        self.playerHand     = []
        self.computerHand   = []
        self.playerBooks    = []
        self.computerBooks  = []
        self.turnCount      = 0      
        self.giveUp         = False
        self.turn           = True #True for human turn, False for computer turn

        for i in VALUES:
            for j in ["Clubs", "Diamonds", "Hearts", "Spades"]:
                self.deck.append(Card(i, j))
        random.shuffle(self.deck)

        introduction = ("Welcome to aelna354's Go Fish game in GUI form!\n"+
        "Consult the README.MD to view the rules.\n"+
        "Press Start Game to begin the game.\n")
        self.terminal.insert(END, introduction)
        self.terminal.config(state=DISABLED)


program = Tk()
program.title("Go Fish Game")
program.resizable(False, False)
app = GoFish(program)
program.mainloop()