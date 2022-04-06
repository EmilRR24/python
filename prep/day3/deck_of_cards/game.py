from classes.deck import Deck
from classes.player import Player

bicycle = Deck()
p1 = Player("John", bicycle)
p2 = Player("Bob", bicycle)

bicycle.distributeCards(Player)

minCards = 0

while (p1.cardCount() != minCards) and (p2.cardCount() != minCards):
    print(f"P1 Card Count: {p1.cardCount()} -- P2 Card Count: {p2.cardCount()}")
    Player.playRound()

if p1.cardCount() == minCards:
    print(f"{p2.name} won the game!!!!!")
else:
    print(f"{p1.name} won the game!!!!!")