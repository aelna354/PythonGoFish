VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Ace", "Jack", "King", "Queen"];

SUITES = ["Clubs", "Diamonds", "Hearts", "Spades"];

function say(msg):
{
  //Code to update textbox
}

function Card(v, s)
{
    this.Value = v;
    this.Suite = s;
}

function Game()
{
  this.deck = [];
  this.playerHand = [];
  this.computerHand = [];
  this.playerBooks = [];
  this.computerBooks = [];
  this.turnCount = 0;
  this.turn = Math.random() >= 0.5;

  for (i = 0; i < 12; i++)
  {
    for (j = 0; j < 4; j++)
    {
      this.deck.push(new Card(VALUES[i], SUITES[j]));

    }
  }
  this.deck.sort(function(a, b){return 0.5 - Math.random()}); //https://www.w3schools.com/js/js_array_sort.asp

  for (i = 0; i < 7; i++)
  {
    this.computerHand.append(this.deck.pop());
    this.playerHand.appen(this.deck.pop());
  }

  this.checkPlayerBooks();
  this.checkComputerBooks();
}

/*
class.js
class Hero {
    constructor(name, level) {
        this.name = name;
        this.level = level;
    }

    // Adding a method to the constructor
    greet() {
        return `${this.name} says hello.`;
    }
}

*/
