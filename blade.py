"""
Pseudocode for a game of Blade. See README.MD for details.

Note a few things. Pseudocode and program are written with these in mind.

-When a player takes a turn, that necessarily means they have less points than their opponent.
-At all times, both players will have an equal number of cards in their deck.
(As it is not possible for one and only one player to draw at once.)
-When state = 0, that means redraw. When it = 1, player's turn. 2 = CPU turn.
-The effect cards, Bolt/Mirror, only work when the opponent's field is nonempty.
-Therefore, when they are played when the opponent's field is empty, they have a value of 1 and are treated like normal Blade cards.
-A player cannot play a Bolt/Mirror card as their last move (if its the last card in their hand).

BLADE GAME PSEUDOCDOE STARTS HERE

construct deck of 32 cards
halve deck, give half to each player
each player draws 10 cards

player.score = 0
cpu.score = 0

state = 0

while the game has not ended:
    if state is 0:
        if both players have an empty hand:
            end game in draw
        elif one player has an empty hand:
            player with nonempty hand wins

        clear all cards on field (both scores = 0)

        if the decks are nonempty:
            each player picks a card in their hand and places it on their field
        else:
            each player places the top card of their deck on their field

        if player's card has higher value:
            state = 2 #cpu turn
        elif cpu card has higher value:
            state = 1 #player turn
        #Note that if they are even, we redraw since state isn't changed.

    elif state is 1:
        turn(player)

    else: #state is 2
        turn(cpu)

def turn(turnPlayer):

    if the only card in turnPlayer's hand is a Bolt/Mirror card OR if turnPlayer's hand is empty:
        opponent wins

    turnPlayer must pick a card in their hand and play it

    if played card is a Blade 1 card and turnPlayer's topmost card is Reversed:
        un-Reverse the Reversed card and reinstate its value
        update turnPlayer's score accordingly
        discard played Blade 1 card

    elif played card is a Blade card or opponent's field is empty:
        if the player's topmost card is reversed:
            remove that reversed card
        place played card on field
        turnPlayer.score += value of placed card

    elif played card is a Bolt card:
        apply reversal to opponent's topmost field card
        a card under reversal has its value reduced to 0
        update opponent.score accordingly
        discard played Bolt card

    elif played card is a Mirror card:
        switch control of all cards on the field
        swap the scores
        discard played Mirror card

    if turnPlayer.score < opponent.score:
        end game, turnPlayer loses
    elif turnPlayer.score = opponent.score:
        state = 0
    else:
        update state variable so opponent takes next turn
"""

#Deck composition, defined via constants.
#ONECARDS is number of Blade 1 cards, TWOCARDS is number of Blade 2 cards, etc..
#BOLTCARDS and MIRRORCARDS are of course the number of Bolt and Mirror cards.

#The total deck size should be an even number and INITDRAW should be strictly less than HALFDECK.
#Game will behave in unexpected ways otherwise.
ONECARDS    = 2
TWOCARDS    = 3
THREECARDS  = 4
FOURCARDS   = 4
FIVECARDS   = 4
SIXCARDS    = 3
SEVENCARDS  = 2
BLADECARDS  = [ONECARDS, TWOCARDS, THREECARDS, FOURCARDS, FIVECARDS, SIXCARDS, SEVENCARDS]
BOLTCARDS   = 6
MIRRORCARDS = 4

NUMCARDS    = sum(BLADECARDS) + BOLTCARDS + MIRRORCARDS
HALFDECK    = NUMCARDS // 2
INITDRAW    = 10

from tkinter import *
from tkinter import messagebox

class Blade():
    def __init__(self, window):
        self.window = window

        bg = PhotoImage(file="images/bg.png")
        back = PhotoImage(file="images/back.png")
        one = PhotoImage(file="images/one.png")

        background = Label(window, image=bg)
        background.image = bg
        background.place(relx=.5, rely=.5, anchor='center')
        
        Deck = Label(window, image=back)
        Deck.image = back
        Deck.place(relx=.5, rely=.5, anchor='center')

        self.terminal = Text(window, height=5, width=40, fg='green', bg='lightgreen')
        self.terminal.place(relx=0, rely=.5, anchor='w')
        self.terminal.insert(END, "Welcome to Blade!\nClick on the deck to start the game.\nConsult README.MD for rules.")
        self.terminal.config(state=DISABLED)

        self.gamestate = Text(window, height=5, width=40, fg='blue', bg='lightblue')
        self.gamestate.place(relx=1, rely=.5, anchor='e')
        self.gamestate.insert(END, "Deck sizes: 16.\nYour score: 0.\nOpponent score: 0.")
        self.gamestate.config(state=DISABLED)

        self.reset = Button(window, text="Reset Game", fg='black', bg='yellow')
        self.reset.place(relx=1, rely=1, anchor='se')

        self.playerHandV = []
        self.cpuHandV    = []
        j = 5
        for i in range(10):
            self.playerHandV.append(Label(window, image=back))
            self.cpuHandV.append(Label(window, image=back))
            self.playerHandV[-1].image = back
            self.cpuHandV[-1].image = back
            self.playerHandV[-1].place(anchor='w', rely=.9, x=(j + 67*i))
            self.cpuHandV[-1].place(anchor='w', rely=.1, x=(j + 67*i))
            j += 16

    def startGame(self):
        self.playerScore    = 0
        self.cpuScore       = 0
        self.playerDeck     = []
        self.cpuDeck        = []
        self.playerHand     = []
        self.cpuHand        = []
        self.playerField    = []
        self.cpuField       = []
        self.playerReversed = False #True if topmost card is reversed
        self.cpuReversed    = False
        self.state          = 0
        self.result         = 0 #1 for player win, 2 for cpu win, 3 for draw

        for amount, value in enumerate(BLADECARDS, 1):
            for i in range(amount):
                self.playerDeck.append(value)

        for i in range(BOLTCARDS):
            self.playerDeck.append(8)

        for i in range(MIRRORCARDS):
            self.playerDeck.append(9)

        random.shuffle(self.playerDeck)

        for i in range(HALFDECK):
            self.cpuDeck.append(self.playerDeck.pop())

    def updateTerminal(self, text):
        self.terminal.config(state=NORMAL)
        self.terminal.delete(1.0, END)
        self.terminal.insert(END, text)
        self.terminal.config(state=DISABLED)

    def updateStatus(self, text):
        self.gamestate.config(state=NORMAL)
        self.gamestate.delete(1.0, END)
        string = (f"Deck sizes: {len(self.playerDeck)}.\n"+
                  f"Your score: {self.playerScore}.\n"
                  f"CPU score:  {self.cpuScore}.")
        self.gamestate.insert(END, string)
        self.gamestate.config(state=DISABLED)

program = Tk()
program.title("Blade!")
program.resizable(False, False)
program.geometry("960x575")
p = Blade(program)
program.mainloop()
