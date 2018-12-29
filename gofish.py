import os
import time
import random

class Card():
	def __init__(self, v, s):
		self.Value = v
		self.Suite = s
		self.Name = f"{v} of {s}"

def printHand():
	output = ""
	for i in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "King", "Queen", "Ace"]:

def say(msg, wait=2):
	print(msg)
	time.sleep(wait)

def clear():
	os.system('cls')

def main():
	stopped = False
	while not stopped:
		result = input("Welcome to aelna354's Go Fish Game!\n\nEnter Exit to close the program.\nEnter anything else to start a game.\n\n")
		if result.lower() == "exit":
			stopped = True
		if not stopped:
			game()

def checkSuites():



def game():
	clear()

	deck = []
	playerHand = []
	compHand = []
	playerSuites = []
	compSuites = []

	#Construct and shuffle Deck
	for i in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "King", "Queen", "Ace"]:
		for j in ["Clubs", "Diamonds", "Hearts", "Spades"]:
			deck.append(Card(i, j))

	random.shuffle(deck)

	say("Beginning game!")
	say("Tossing coin to determine who goes first...")
	turn = random.choice([True, False]) #True for human turn, False for computer turn
	if turn:
		say("You go first! Each player now draws 7 cards...")
	else:
		say("Computer goes first! Each player nows draw 7 cards...")

	for i in range(0, 7): #7 draws
		playerHand.append(deck.pop())
		compHand.append(deck.pop())

	print(f"Player hand:\n{playerHand}\nComputer hand:\n{compHand}\nDeck size: {len(deck)}\n")
	input()

	clear()

main()