# aeln354's Go Fish Game And Blade Game

Made for fun/outta boredom. Inspired by the Go Fish game in Spy Fox in Dry Cereal. Coded in Python 3. Also made a Blade game inspired by the game of such name in Trails of Cold Steel.


# Rules for Go Fish

This version of the game pits the player against the CPU. `gofish.py` is the command line version of the game and the first one originally developed. `gui.py` is the GUI version of the game though the GUI is extremely minimalistic; it still uses a terminal screen and it doesn't display the cards. The main draw of this version is that it can be played with the mouse alone (no keyboard usage necessary). To play the command line version, run `python gofish.py` in the terminal; use `app.cmd` to run the GUI version.

## Basics and Objective

There is the standard deck of 52 cards. In this deck, there are 13 "Face Values" - 2 thru 10, Ace, Jack, King and Queen. For each Value, there are 4 cards of that Value, each of a different Suite - Spades, Clubs, Diamonds and Hearts. So for example, there are 4 Ace cards; Ace of Spades, Ace of Clubs, Ace of Diamonds and Ace of Hearts. Same deal with 3s, 10s, Jacks, 1s, etcetera.

A Book is a collection of 4 cards, each with the same Face Value, where each card is of a unique Suite. For instance, the 4 cards Jack of Spades, Jack of Clubs, Jack of Diamonds and Jack of Hearts form a Book. With 13 different Face Values, there are 13 different possible Books.

The goal of the game is to have more Books than the other player once the game ends.

At the beginning, each player draws 7 cards. Each player's hand is concealed from the other player, but the other player knows how many cards are in their opponent's hand. The game is played in turns. At the beginning, a coin is tossed to determine who goes first.

During a player's turn, they (hereafter referred to as the "Turn Player") must ask the other player (hereafter referred to as the "Opponent") if they hold any cards of a certain Value, provided the Turn Player is holding at least one card of that Value. If the Opponent has at least one card of that Value in their hand, they must turn over all cards of that Value they hold to the Turn Player, and the Turn Player gets an extra Turn. If the Opponent has no cards of that Value, they tell the Turn Player to "Go Fish", and the Turn Player draws a card from the deck. If the drawn card is not of the Value the Turn Player just asked for, then the Opponent now takes their turn. If it is, then the Turn Player takes an extra turn. (For example, if the Turn Player asks for 2s, and the Opponent has none, and if the card the Turn Player draws when they Go Fish is a 2, then the Turn Player gets another turn).

As soon as a player is holding all 4 cards of a Book, whether this is after the initial 7-card-draw, after Go Fishing, or after recieving cards from their opponent, they must immediately discard the 4 cards of that Book and this counts as one of their Books for the game.

When a player has an empty hand, or once the deck is empty, the game ends. At that point, whichever player has more Books than the other wins. If it's a tie, the game ends in a Draw. Additionally, if a player has 7 Books, then the game ends and that player wins - 7 is a majority of Books, meaning that it would not be possible for their opponent to have more.

## Cheat Codes

Enter "revealHand" when prompted to see the contents of the computer's hand. May be fun/charming, but will remove strategy from the game and make it a cakewalk! (Currently only supported on console version.)

## Features To Be Implemented
* An "Extended Play Mode" where only one card of the asked-for Value is surrendered. Would make the game more strategic, but also a lot longer and slower (possibly to the point of tedium)

# Rules for Blade

As with above, run `python blade.py` to play the command line version of Blade.

Blade is a card game where each player tries to have a higher score than the other. It is constructed with a 32-card deck consisting of Blade cards each valued from 1-7, Bolt cards, and Mirror cards. At the start of the game, the deck is halved with 16 cards given to each player. Then, each player draws 10 cards. (I have written the program so that you can easily change the composition and size of the deck by merely changing constants in the code; the only constraint is that it must be of an even size.)

After this happens, each player places the top card of their deck on their field. At all times, a player's score is equal to the value of all cards on their field. Whoever has the lower score takes the first turn.

During a turn, a player can:

* Play a Blade card to their field and raise their score by its value

* Play a Bolt card to "Reverse" the topmost card (last card placed) on their opponent's field and reduce its value to 0

* Play a Mirror card to swithc control of all cards on the field, effectively swapping the scores

* If the topmost card on their field is Reversed, they can use a 1-valued Blade card to un-reverse that card

If, after a player takes a turn, their score is lower than their opponent's, they lose. If it is higher, the opponent must take their turn. If a player takes a turn when their hand is empty, they lose. It is not allowed to play a Bolt/Mirror card as a player's final card; therefore, when it is a player's turn, and the last card in their hand is a Bolt or Mirror card, they automatically lose.

If, after a player takes a turn, their score is tied, then both players must clear their field and re-draw a card from their deck. If the decks are empty, they must use a card in their hand for this purpose instead.

When a Mirror or Bolt card is played from the deck or played when the opponent has an empty field, it is treated as a 1-valued Blade card.

Pseudocode for the game is given at the top of the blade.py file.
