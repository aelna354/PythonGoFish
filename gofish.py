import os
import time
import random

VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Ace", "Jack", "King", "Queen", "Ace"]

class Card():
	def __init__(self, v, s):
		self.Value = v
		self.Suite = s

def say(msg, wait=1.5):
	print(msg)
	time.sleep(wait)

def clear():
	os.system("clear||cls") #Platform indepent screen clearing
		
class Game():
	def __init__(self):
		self.deck = []
		self.playerHand = []
		self.compHand = []
		self.playerSuites = 0
		self.compSuites = 0
		self.giveUp = False
		self.turn = True
		#self.turn = random.choice([True, False]) #True for human turn, False for computer turn

		self.game()

	def playerDraw(self):
		self.playerHand.append(self.deck.pop())

	def computerDraw(self):
		self.compHand.append(self.deck.pop())

	def checkPlayerSuites(self):
		if len(self.playerHand) == 0:
			return

		for i in VALUES:
			if sum(card.Value==i for card in self.playerHand) == 4:
				say(f"You have a Completed Suite for value {i}! Moving all cards of that Completed Suite out of your hand.")
				self.playerHand = [card for card in self.playerHand if card.Value!=i]
				self.playerSuites += 1
				say(f"You now have a Completed Suite for value {i}. You have completed {self.playerSuites} suites.")

		if len(self.playerHand) == 0: #If the player didn't start with 0 cards, but now does, then their hand is empty after completing suites.
			say("Your hand was emptied after completing a Suite. You may draw one card now.")
			self.playerDraw()

	def checkCompSuites(self):
		if len(self.compHand) == 0:
			return

		for i in VALUES:
			if sum(card.Value==i for card in self.compHand) == 4:
				say(f"The computer has a Completed Suite for value {i}! Moving all cards of that Completed Suite out of their hand.")
				self.compHand = [card for card in self.compHand if card.Value!=i]
				self.compSuites += 1
				say(f"The computer now has a Completed Suite for value {i}. They have completed {self.compSuites} suites.")

		if len(self.compHand) == 0:
			say("The computer's hand was emptied after completing a Suite. They may draw one card now.")
			self.playerDraw()

	def printHand(self):
		if (len(self.playerHand) == 0):
			return ""

		output = ""
		for i in VALUES:
			cards = [card.Suite for card in self.playerHand if card.Value==i]
			if len(cards) > 0:
				string = ""
				for s in cards: string += f"{s}, "
				string = string[:-2] #Exlcude space and comma added after last element
				output += f"{i.ljust(5)} ({len(cards)}): {string}\n"

		return output

	def validGuess(self):
		guess = input()

		if guess.lower() == "exit":
			self.giveUp = True
			return

		if guess.lower() in ["jack", "king", "queen", "ace"]: #Allows the acceptance of case insensitive input
			guess = guess.lower()
			guess = guess.capitalize()

		if guess not in VALUES: #If guess is not even valid
			print("ERROR: Input value not in accepted range. Please either enter a number from 2-10, or one of the words"+
			" Jack, King, Queen, Ace or Exit in any casing.")
			return "-1"

		if sum(card.Value==guess for card in self.playerHand) == 0: #If player is holding no cards of this value
			print("ERROR: You are not holding a card of the provided input value.")
			return "-1"
		
		return "guess"

	def playerTurn(self):
		clear()

		if (0 == len(self.playerHand)) and (len(deck) > 0):
			print("Your hand is empty. Drawing one card right now.")
			self.playerDraw()

		print(
		f"It is now your turn. There are currently {len(self.deck)} cards in the deck.\n"+
		f"You have completed {self.playerSuites} Suites and are holding {len(self.playerHand)} cards.\n"+
		f"The computer has completed {self.compSuites} Suites and is holding {len(self.compHand)} cards.\n"+
		f"You have the following cards in your hand:\n\n{self.printHand()}"+
		f"Enter the Value of a card you are holding to ask the computer if they have any cards of that value.\n"+
		f"(For face cards, enter \"Jack\", \"King\", etc. Enter exit to forefit the game. Words are case insensitive.))\n"
		)

		guess = self.validGuess()
		while (not self.giveUp) and (guess != "-1"):
			guess = self.validGuess()

		if self.giveUp:
			return

		input("Confirmed")


	def getResults(self):
		print(f"Game results:\nFinal deck size: {len(self.deck)}\n"+
			  f"Your Completed Suites ({len(self.playerSuites)}): {self.playerSuites}\n"+
			  f"Computer Completed Suites ({len(self.compSuites)}): {self.compSuites}\n\n")

	def game(self):
		clear()

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
			say("Computer goes first! Each player nows draw 7 cards...")

		for i in range(0, 7): #7 draws
			self.playerDraw()
			self.computerDraw()

		say("Checking for Completed Suites in initial draw...")
		self.checkPlayerSuites()
		self.checkCompSuites()
		say("Beginning game now.")

		while (7 > self.compSuites and 7 > self.playerSuites and (not self.giveUp)):
			if self.turn:
				self.playerTurn()
			else:
				self.computerTurn()
			self.turn = not self.turn

		if self.giveUp:
			clear()
			print("You have forefited the game. Congratulations to the Computer, they win! Better luck next time.")
			self.getResults()
		else if 7 == self.compSuites:
			clear()
			print("Congratulations! You have won the game.")
			self.getResults()
		else:
			clear()
			print("Sorry, but it looks like you lost this game. Better luck next time.")
			self.getResults()
		clear()

def main():
	stopped = False
	while not stopped:
		result = input("Welcome to aelna354's Go Fish Game!\n\nEnter Exit to close the program.\nEnter anything else to start a game.\n\n")
		if result.lower() == "exit":
			stopped = True
		if not stopped:
			Game()

main()