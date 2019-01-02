# aeln354's Go Fish Game

Made for fun/outta boredom. Inspired by the Go Fish game in Spy Fox in Dry Cereal. Coded in Python. Play it with `python gofish.py`. Programmed in Python 3.

This version of the game pits the player against the CPU.

# Rules

## Basics and Objective

There is the standard deck of 52 cards. In this deck, there are 13 "Face Values" - 2 thru 10, Ace, Jack, King and Queen. For each Value, there are 4 cards of that Value, each of a different Suite - Spades, Clubs, Diamonds and Hearts. So for example, there are 4 Ace cards; Ace of Spades, Ace of Clubs, Ace of Diamonds and Ace of Hearts. Same deal with 3s, 10s, Jacks, 1s, etcetera.

A Book is a collection of 4 cards, each with the same Face Value, where each card is of a unique Suite. For instance, the 4 cards Jack of Spades, Jack of Clubs, Jack of Diamonds and Jack of Hearts form a Book. With 13 different Face Values, there are 13 different possible Books.

The goal of the game is to have more Books than the other player once the game ends.

## Gameplay Flow

At the beginning, each player draws 7 cards. Each player's hand is concealed from the other player, but the other player knows how many cards are in their opponent's hand. The game is played in turns. At the beginning, a coin is tossed to determine who goes first.

During a player's turn, they (hereafter referred to as the "Turn Player") must ask the other player (hereafter referred to as the "Opponent") if they hold any cards of a certain Value, provided the Turn Player is holding at least one card of that Value. If the Opponent has at least one card of that Value in their hand, they must turn over all cards of that Value they hold to the Turn Player, and the Turn Player gets an extra Turn. If the Opponent has no cards of that Value, they tell the Turn Player to "Go Fish", and the Turn Player draws a card from the deck. If the drawn card is not of the Value the Turn Player just asked for, then the Opponent now takes their turn. If it is, then the Turn Player takes an extra turn. (For example, if the Turn Player asks for 2s, and the Opponent has none, and if the card the Turn Player draws when they Go Fish is a 2, then the Turn Player gets another turn).

As soon as a player is holding all 4 cards of a Book, whether this is after the initial 7-card-draw, after Go Fishing, or after recieving cards from their opponent, they must immediately discard the 4 cards of that Book and this counts as one of their Books for the game.

When a player has an empty hand, or once the deck is empty, the game ends. At that point, whichever player has more Books than the other wins. If it's a tie, the game ends in a Draw. Additionally, if a player has 7 Books, then the game ends and that player wins - 7 is a majority of Books, meaning that it would not be possible for their opponent to have more.

# Cheat Codes

Enter "revealHand" when prompted to see the contents of the computer's hand. May be fun/charming, but will remove strategy from the game and make it a cakewalk!

# Features To Be Implemented
* An "Extended Play Mode" where only one card of the asked-for Value is surrendered to make the game longer and more strategic
* A deck-viewing cheat
* Create a GUI for this game in Tkinter or maybe even Ren'py