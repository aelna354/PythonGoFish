"""
PSEUDOCODE
Note a few things. Program is coded/pseudocode is written with these in mind.

-When a player takes a turn, that necessarily means they have less points than their opponent.
-At all times, both players will have an equal number of cards on their deck.
(It is not possible for one and only one player to draw at once.)
-When state = 0, that means redraw. When it = 1, player's turn. 2 = CPU turn.
-The effect cards, Bolt/Mirror, only work when the opponent's field is nonempty.
-When they are played when the opponent's field is empty, they have a value of 1.


BLADE GAME PSEUDOCDOE STARTS HERE

construct deck of 32 cards
halve deck, give half to each player
each player draws 10 cards

player.score = 0
cpu.score = 0

state = 0

while the game has not ended:
	if state is 0:
		clear all cards on field (both scores = 0)
	 	
		if the decks are empty and one player has an empty hand:
			the player with a non-empty hand wins
		elif both decks are empty:
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

ONECARD 	= 2
TWOCARD 	= 3
THREECARD 	= 4
FOURCARD 	= 4
FIVECARD 	= 4
SIXCARD 	= 3
SEVENCARD 	= 2
BLADECARDS 	= [ONECARD, TWOCARD, THREECARD, FOURCARD, FIVECARD, SIXCARD, SEVENCARD]
BOLTCARDS 	= 6
MIRRORCARDS = 4

import os
import time
import random

def say(msg):
	print(msg)
	time.sleep(1.5)

def clear():
	os.system("clear||cls")

class Game():
	def __init__(self):
		clear()
		self.playerDeck  = []
		self.cpuDeck	 = []
		self.playerHand  = []
		self.cpuHand	 = []
		self.playerField = []
		self.cpuField 	 = []
		self.playerScore = 0
		self.cpuScore 	 = 0
		self.state		 = 0
		self.result		 = 0 #1 for player win, 2 for cpu win, 3 for draw

		#We store the cards in self.playerDeck initially. They are shuffled and split into opponent's deck later.
		for amount, value in enumerate(BLADECARDS, 1):
			for i in range(amount):
				self.playerDeck.append(value)

		#bolt cards are represented as 8.
		#mirror cards are represented as 9.
		for i in range(BOLTCARDS):
			self.playerDeck.append(8)
		for i in range(MIRRORCARDS):
			self.playerDeck.append(9)

		random.shuffle(self.playerDeck)

		for i in range(16):
			self.cpuDeck.append(self.playerDeck.pop())

		say("Beginning game!")
		say("Each player takes a half-deck of 16 cards, then draws 10 cards...")

		for i in range(10):
			self.playerHand.append(self.playerDeck.pop())
			self.cpuHand.append(self.cpuDeck.pop())

		say("\nYour hand consists of the following cards:\n")
		say(self.showPlayerHand())
		say("Press enter to start the game.")
		
		input("")

		while self.result == 0:
			clear()
			if self.state == 0:
				say(f"Both players have an even score! Clearing the field...")
				self.playerField = []
				self.cpuField = []
				self.playerScore = 0
				self.cpuScore = 0

				if len(self.playerDeck) == 0 and (0 == len(self.playerHand) or 0 == len(self.cpuHand)):
					self.result = 3
					return
				elif len(self.playerDeck) == 0: #if decks are empty but hands aren't
					say("Your deck is empty! You must place a card in your hand on the field.")
					card = self.ask()
			elif self.state == 1:
				self.playerTurn()
			else:
				self.cpuTurn()

	def ask(self):
		say("Enter the number of the selected card if it is a Blade card.\n"+
			"Enter \"Bolt\" or \"Mirror\" (case insensitive) to pick one of those cards.\n"+
			"You can only pick a card in your hand.")

		while True:
			c = input().lower()

			if c not in ["1", "2", "3", "4", "5", "6", "7", "mirror", "bolt"]:
				c = ""
				print("Invalid input. Please re-enter.")
			
			elif c == "mirror":
				if 0 == sum(card.type=="Mirror" for card in self.playerHand):
					c = ""
					print("You are not holding a Mirror card. Please re-enter.")

			elif c == "bolt":
				if 0 == sum(card.type=="Bolt" for card in self.playerHand):
					c = ""
					print("You are not holding a Bolt card. Please re-enter.")

			else:
				if 0 == sum(card.type=="Blade" and card.value==c for card in self.playerHand):
					c = ""
					print("Your are not holding a card of that value. Please re-enter.")
		return c

	def showPlayerHand(self):
		#Blade X cards: (n)
		#Bolt cards:    (n)
		#Mirror cards:  (n)
		output = ""

		for i in range(1, 8):
			cards = len([card for card in self.playerHand if card==i])
			if cards > 0:
				output += f"Blade {i} cards: ({cards})\n"

		bolts = len([card for card in self.playerHand if card==8])
		if bolts > 0:
			output += f"Bolt cards:    ({bolts})\n"

		mirrors = len([card for card in self.playerHand if card==9])
		if mirrors > 0:
			output += f"Mirror cards:  ({mirrors})\n"

		return output

def main():
    while True:
        result = input("Welcome to aelna354's Blade game!\n"+
        "(Consult the README.MD file to view the rules.)\n"
        "Enter exit in any casing to close the program.\n"+
        "Otherwise, press enter to start the game.\n")
        
        if result.lower() != "exit":
            Game()
            continue

        break

main()