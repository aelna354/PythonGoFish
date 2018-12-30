# aeln354's Go Fish Game

Made for fun/outta boredom. Inspired by the Go Fish game in Spy Fox in Dry Cereal. Coded in Python. Play it with `python gofish.py`. Rules are as follows.

There is the standard deck of 52 cards. In this deck, there are 13 "Face Values" - 2 thru 10, Ace, Jack, King and Queen. For each Value, there are 4 cards of that Value (13 * 4 = 52), each of a different Suite - Spades, Clubs, Diamonds and Hearts. So for example, there are 4 Ace cards; Spades, Clubs, Diamonds and Hearts. Same deal with 3s, 8s, 10s, Jacks, 1s, etcetera.

This version of the game is restricted to a play between 2 players and of course the second player is the CPU.

The goal of the game is to be the first player to have a majority of Completed Suites. A Completed Suite is a set of 4 cards all of a particular Value (where each card is of a different Suite). Since there are 13 different Values, that means there are 13 different Completed Suites - the first player to complete a majority of these Suites, which would be 7, is the winner. An example of a Completed Suite would be the 4 cards 2 of Diamonds, 2 of Hearts, 2 of Clubs and 2 of Spades. This is the Completed Suite for 2. Every other Value similarly has its own Completed Suite.

The rules of the games are as follows. At the beginning, each player draws 7 cards. Each player's hand is concealed from the other player, but the other player can see the number of cards in their opponent's hand. The game is played in turns. At the beginning, a coin is tossed to determine who goes first.

During a player's turn, they (herein referred to as the "Turn Player") must ask the other player (herein referred to as the "Opponent") if they have any cards of a certain Value, provided the Turn Player has at least one card of that Value in their hand. If the Opponent has at least one card of that Value in their hand, they must turn over all cards of that Value to the Turn Player, and the Turn Player gets an extra Turn. If the Opponent has no cards of that Value, they tell the Turn Player to "Go Fish", and the Turn Player draws a card. If the drawn card is not of the Value the Turn Player just asked for, then the Opponent takes their turn. If it *is*, then the Turn Player takes an extra turn. (For example, if the Turn Player asks for 2s, and the Opponent has none, and if the card the Turn Player draws when they Go Fish is a 2, then the Turn Player gets another turn).

As sonn as a player is holding all 4 cards of a Completed Suite, whether this is after the initial 7-card-draw, after Go Fishing, or after recieving cards from their opponent, they must immediately place those 4 cards on the table in a pile and that pile is considered their Completed Suite. The first player to have 7 of these Completed Suite piles wins.

Provided the deck is not empty: whenever a player's hand is empty at the start of their turn, or whenever a player's hand is empty after they place a Completed Suite, they draw 1 card.