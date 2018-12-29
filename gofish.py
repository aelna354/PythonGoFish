#Interactive, CLI based implementation of Go Fish.
#See the README.MD for full rules.

import os
import time
import random

#The 13 possible face values. Each of these represents one Completed Suite.
VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Ace", "Jack", "King", "Queen"]

#Prints a message with a wait before continuing.
def say(msg, wait=1.5):
	print(msg)
	time.sleep(wait)

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
		self.deck = []
		self.playerHand = []
		self.computerHand = []
		self.playerSuites = []
		self.computerSuites = []
		self.giveUp = False #If the user exits the game by entering in exit, then this is True and the game halts.
		self.turnCount = 0		

		clear()
		#Construct and shuffle Deck
		for i in VALUES:
			for j in ["Clubs", "Diamonds", "Hearts", "Spades"]:
				self.deck.append(Card(i, j))

		random.shuffle(self.deck)

		print("Beginning game!")
		say("Tossing coin to determine who goes first...")
		self.turn = random.choice([True, False]) #True for human turn, False for computer turn
		if self.turn:
			print("You go first! Each player now draws 7 cards...")
		else:
			print("The Computer goes first! Each player nows draw 7 cards...")

		for i in range(7): #7 draws
			self.playerDraw(show=False)
			self.computerDraw()

		print("Checking for Completed Suites in initial draws...")
		self.checkPlayerSuites()
		self.checkComputerSuites()
		input("Press enter to begin the game now.")

		while (7 > len(self.computerSuites) and 7 > len(self.playerSuites) and (not self.giveUp)):
			self.turnCount += 1
			if self.turn:
				self.playerTurn()
			else:
				self.computerTurn()
			#self.turn is modified in the playerTurn()/computerTurn() method

		clear()

		if self.giveUp:
			print("You have forefited the game. Congratulations to the Computer, they win! Better luck next time.")
		elif len(self.playerSuites) >= 7:
			print("Congratulations! You have won the game.")
		else:
			print("Sorry, but it looks like you lost this game. Better luck next time!")

		print(f"Game results:\n"+
			  f"Turn Count: {self.turnCount}\n"+
			  f"Final deck size: {len(self.deck)}\n"+
			  f"Your Completed Suites ({len(self.playerSuites)}): {self.playerSuites}\n"+
			  f"Computer Completed Suites ({len(self.computerSuites)}): {self.computerSuites}\n\n")

		
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

	#Checks if the player has a completed suite, and if so, removes it from their hand and raises their count of completed suites.
	def checkPlayerSuites(self):
		if len(self.playerHand) == 0:
			return

		for i in VALUES:
			if sum(card.Value==i for card in self.playerHand) == 4:
				say(f"You have a Completed Suite for value {i}! Moving all cards of that Completed Suite out of your hand.")
				self.playerHand = [card for card in self.playerHand if card.Value!=i]
				self.playerSuites.append(i)
				say(f"You now have a Completed Suite for value {i}. You have completed {len(self.playerSuites)} suites.")

		if len(self.playerHand) == 0 and len(self.deck) > 0:
			say("Your hand was emptied after completing a Suite. You may draw one card now.")
			self.playerDraw()

	#Same as checkPlayerSuites, but for the Computer. (Strings are different.)
	def checkComputerSuites(self):
		if len(self.computerHand) == 0:
			return

		for i in VALUES:
			if sum(card.Value==i for card in self.computerHand) == 4:
				say(f"The computer has a Completed Suite for value {i}! Moving all cards of that Completed Suite out of their hand.")
				self.computerHand = [card for card in self.computerHand if card.Value!=i]
				self.computerSuites.append(i)
				say(f"The computer now has a Completed Suite for value {i}. They have completed {len(self.computerSuites)} suites.")

		if len(self.computerHand) == 0 and len(self.deck) > 0:
			say("The computer's hand was emptied after completing a Suite. They may draw one card now.")
			self.computerDraw()

	#Outputs a list of cards in the player's hand. Sorted by value, and includes a count of the number of cards of that value.
	def printHand(self):
		if len(self.playerHand) == 0:
			return "\n"

		output = ""
		for i in VALUES:
			cards = [card.Suite for card in self.playerHand if card.Value==i]
			if len(cards) > 0:
				string = ""
				for s in cards: string += f"{s}, "
				string = string[:-2] #Exlcude space and comma added after last element
				output += f"{i.ljust(5)} ({len(cards)}): {string}\n"

		return output

	#Pulls in a valid card guess from the user. Returns -1 if invalid result (in which case error message is printed and this function is then re-called).
	def validGuess(self):
		guess = input()

		if guess.lower() == "exit":
			self.giveUp = True
			return "Error"

		if guess.lower() in ["jack", "king", "queen", "ace"]: #Allows the acceptance of case insensitive input
			guess = guess.lower()
			guess = guess.capitalize()

		if guess not in VALUES:
			print("ERROR: Input value not in accepted range. Enter an integer from 1-10,\n"+
				  "or one of the words Jack, King, Queen, Ace or Exit in any casing.\n")
			return "-1"

		if sum(card.Value==guess for card in self.playerHand) == 0: #If player is holding no cards of this value
			print("ERROR: You are not holding a card of the provided input value.\n")
			return "-1"
		
		return guess

	#Function used to transfer cards of the guessed type from one player to the other.
	#Takes in the current hands by value, and returns the updated hands.
	def surrender(self, givingHand, takingHand, value):
		for i in givingHand:
			if i.Value==value:
				takingHand.append(i)
		givingHand = [card for card in givingHand if card.Value!=value]
		return givingHand, takingHand

	#Function for running player turn.
	def playerTurn(self): 
		clear()

		if 0 == len(self.playerHand) and len(deck) > 0:
			print("Your hand is empty. Drawing one card right now.")
			self.playerDraw()

		print(
		f"Turn Count: {self.turnCount}, Deck Size: {len(self.deck)}\n"+
		f"Current Turn: Player\n"+
		f"Player has completed   {len(self.playerSuites)} Suites and is holding {len(self.playerHand)} cards.\n"+
		f"Computer has completed {len(self.computerSuites)} Suites and is holding {len(self.computerHand)} cards.\n"+
		f"You have the following cards in your hand:\n\n{self.printHand()}\n"+
		f"Enter a Value of a card you're holding to ask the computer if they have any cards of that value.\n"+
		f"Enter \"Exit\" to forefit the game.\nAll input is case insensitive.\n"
		)

		guess = self.validGuess()
		while guess == "-1":
			guess = self.validGuess()

		if self.giveUp:
			return

		say(f"Player asks the computer: got any {guess}s?")
		num = sum(card.Value==guess for card in self.computerHand)

		if num > 0:
			say(f"Computer has {num} cards with such value! Computer surrenders those cards to Player.")
			self.computerHand, self.playerHand = self.surrender(self.computerHand, self.playerHand, guess)
			say("Checking player hand for Suites...")
			self.checkPlayerSuites()
			say("Due to your correct guess, you get an extra turn!")
			
		else:
			self.turn = not self.turn
			say("Sorry, computer has no cards with such value.")
			say("Player, go fish! You draw a card.")
			if len(self.deck) == 0:
				say("Deck is empty. Card draw skipped.")
			else:
				self.playerDraw()
				
				if self.playerHand[-1].Value==guess:
					self.turn = not self.turn
					say(f"Congratulations! The card you just drew is of the value you guessed. You get an extra turn!")
				say("Checking for completed Suites...")
				self.checkPlayerSuites()

		if self.turn:
			input("Press enter to close this text and start your extra turn.")
		else:
			input("Press enter to close this text and start the computer's turn.")

	#Function for running a computer's turn.
	def computerTurn(self):
		clear()

		if 0 == len(self.computerHand) and (len(deck) > 0):
			print("The Computer's hand is empty. Drawing one card right now.")
			self.computerDraw()

		print(
		f"Turn Count: {self.turnCount}, Deck Size: {len(self.deck)}\n"+
		f"Current Turn: Player\n"+
		f"Player has completed   {len(self.playerSuites)} Suites and is holding {len(self.playerHand)} cards.\n"+
		f"Computer has completed {len(self.computerSuites)} Suites and is holding {len(self.computerHand)} cards.\n"+
		f"You have the following cards in your hand:\n\n{self.printHand()}\n")

		say("The computer is thinking of what to ask...")
		guess = random.choice(self.computerHand).Value #For now, its random.
		say(f"The computer asks you: got any {guess}s?")

		num = sum(card.Value==guess for card in self.playerHand)

		if num > 0:
			say(f"You are holding {num} cards with such value! You surrender them to the Computer.")
			self.playerHand, self.computerHand = self.surrender(self.playerHand, self.computerHand, guess)
			say("Checking computer hand for Suites...")
			self.checkComputerSuites()
			say("Due to its correct guess, the computer gains an extra turn!")

		else:
			self.turn = not self.turn
			say("Nope, you have no cards with such value.")
			say("The computer must Go Fish! Computer draws a card.")

			if len(self.deck) == 0:
				say("Deck is empty. Card draw skipped.")
			else:
				self.computerDraw()
				if self.computerHand[-1].Value==guess:
					self.turn = not self.turn
					say(f"The card the computer just drew is of their guessed value, {guess}. The computer gets an extra turn!")
				say("Checking computer hand for Suites...")
				self.checkComputerSuites()

		if self.turn:
			input("Press enter to close this text and start your turn.")
		else:
			input("Press enter to close this text and begin the computer's extra turn.")

def main():
	stopped = False
	while not stopped:
		result = input("Welcome to aelna354's Go Fish Game!\n"+
		"Enter anything other than exit to start a game.\n"+
		"Enter exit in any casing to close the program.\n")
		
		if result.lower() == "exit":
			stopped = True
		if not stopped:
			Game()

main()