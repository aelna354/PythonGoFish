"""
construct deck of 32
halve deck, give half to each player
each player draws 10 cards

state = 0 #0 for dick, 1 for player turn, 2 for cpu turn
result = 0 #1 for player wins, 2 for cpu win, 3 for draw

player.score = 0
cpu.score = 0

while result == 0:
	if state == 0:
		dick()
	elif state == 1:
		turn(player)
	else: #state = 2
		turn(cpu)

if result == 1:
	player wins
elif result == 2:
	cpu wins
else:
	end game in draw

def dick():
	clear all cards on field (both scores = 0)
 	
	#NOTE: At all times, both players will have the same # of cards in deck.
	if the decks are empty and at least one player has an empty hand:
		result = 3
		return
	elif the decks are empty:
		each player picks a card in their hand and places it on their field
	else: #decks are nonempty
		each player places the top card of their deck on their field

	if player card has higher value:
		state = 2 #cpu turn
	elif cpu card has higher value:
		state = 1 #player turn
	#Note that if they are even, dick() gets re-called since state isn't changed.

#Note that whenever this function is called, turnPlayer necessarily has less points than the opponent.
def turn(turnPlayer):
	if turnPlayer's hand is empty OR if the only card in it is Bolt/Mirror:
		opponent wins

	turnPlayer must pick a card in their hand and play it

	if played card is a Blade 1 card and there is a Reversed card on player's field:
		un-Reverse the last card that is Reversed and reinstate its value
		discard played Blade 1 card

	elif played card is a Blade card:
		place Blade card on field
		turnPlayer.score += value of placed card

	elif played card is a Bolt card:
		apply reversal to the last card placed on opponent's field
		a card under reversal has its value reduced to 0
		update opponent.score accordingly

	elif played card is a Mirror card:
		switch control of all cards on the field
		swap the scores

	if turnPlayer.score < opponent.score:
		turnPlayer loses, update result variable
	elif turnPlayer.score = opponent.score:
		state = 0
	else:
		update state variable so opponent takes next turn
"""

#[0] is number of 1 cards, [1] is 2 cards... [7] is # of Bolt cards, [8] is mirror
VALUES = [2, 3, 4, 4, 4, 3, 2, 6, 4]

import os
import time
import random

def say(msg):
	print(msg)
	time.sleep(1.5)

def clear():
	os.system("clear||cls")

class Card():
	def __init__(self, t, v):
		self.type = t
		self.value = v
		self.name = f"{t} ({v})"
		self.reversed = False

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
		self.result		 = 0

		deck = []

		for cardvalue in range(1, 8): #First 7 card values (balde cards)
			for numberofcards in range(VALUES[cardvalue - 1]):
				deck.append(Card("Blade", cardvalue))

		for i in range(VALUES[7]):
			deck.append(Card("Bolt", 1))

		for i in range(VALUES[8]):
			deck.append(Card("Mirror", 1))

		random.shuffle(deck)

		say("Beginning game!")
		say("Each player takes a half-deck of 16 cards, then draws 10 cards...")

		for i in range(16):
			self.playerDeck.append(deck.pop())
			self.cpuDeck.append(deck.pop())

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
				self.dick()
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

	def dick(self):
		say("Time to dick! Clearing the field...")
		self.playerField = []
		self.cpuField = []
		self.playerScore = 0
		self.cpuScore = 0

		#NOTE: At all times, len(playerdeck) = len(cpudeck).
		if len(self.playerDeck) == 0 and (0 == len(self.playerHand) or 0 == len(self.cpuHand)):
			self.result = 3
			return
		elif len(self.playerDeck) == 0: #if decks are empty but hands aren't
			say("Your deck is empty! You must place a card in your hand on the field.")
			card = self.ask()

	def showPlayerHand(self):
		output = ""

		for i in range(1, 8):
			cards = [card for card in self.playerHand if card.type=="Blade" and card.value==i]
			if len(cards) > 0:
				output += f"{cards[0].name} cards: {len(cards)}\n"

		mirrors = [card for card in self.playerHand if card.type=="Mirror"]
		if len(mirrors) > 0:
			output += f"Mirror cards: {len(mirrors)}\n"

		bolts = [card for card in self.playerHand if card.type=="Bolt"]
		if len(bolts) > 0:
			output += f"Bolt cards: {len(bolts)}\n"

		return output

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