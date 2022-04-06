from .deck import Deck
from .card import Card
import random

class Player:
    players = []
    deck = None
    warPile = []
    round = 1
    def __init__(self, name: str, deck: Deck) -> None:
        self.name = name
        self.hand = []
        self.pile = []
        Player.deck = deck
        Player.players.append(self)

    def drawCard(self):
        ## Called at start only
        self.hand.insert(0,Player.deck.giveCard())
        return self

    def addCardPile(self, card) -> None:
        # Add cards to pile
        if type(card) is list:
            self.pile.extend(card)
        else:
            self.pile.append(card)
    
    def addCardHand(self, card) -> None:
        # Add card to hand
        if type(card) is list:
            self.hand.extend(card)
        else:
            self.hand.append(card)

    def playCard(self) -> Card:
        return self.hand.pop()

    def cardCount(self):
        # print(self.hand)
        # print(self.pile)
        h = len(self.hand)
        p = len(self.pile)
        r = h + p
        # print(r)
        return r

    def ensureHandFull(self):
        if not self.hand:
            self.shuffle()
            self.pileToHand()

    def shuffle(self):
        random.shuffle(self.pile)

    def pileToHand(self):
        while self.pile:
            self.addCardHand(self.pile.pop())

    @classmethod
    def playRound(cls):
        # alwways 2 people, hardcoding players
        pl1 = cls.players[0]
        pl2 = cls.players[1]
        # print("are we indefinitely looping?")
        if pl1.cardCount() == 0 or pl2.cardCount() == 0:
            return
        print(f"\nRound :: {cls.round}")
        # print(f"Player 1 Hand: {len(pl1.hand)}")
        # print(f"Player 1 Pile: {len(pl1.pile)}")
        # print(f"Player 2 Hand: {len(pl2.hand)}")
        # print(f"Player 2 Pile: {len(pl2.pile)}")
        pl1.ensureHandFull()
        pl2.ensureHandFull()
        pl1CardList = [pl1.playCard()]
        pl2CardList = [pl2.playCard()]
        Player.war(pl1, pl2, pl1CardList, pl2CardList)
        cls.round += 1

    @staticmethod
    def war(pl1, pl2, pl1CardList, pl2CardList):
        print(f"{pl1.name} played {pl1CardList[-1].getString()}")
        print(f"{pl2.name} played {pl2CardList[-1].getString()}")
        if pl1CardList[-1].getPointVal() > pl2CardList[-1].getPointVal():
            # Player 1 Wins
            print(f"{pl1.name} won the round!!")
            pl1.addCardPile(pl1CardList)
            pl1.addCardPile(pl2CardList)
        elif pl1CardList[-1].getPointVal() < pl2CardList[-1].getPointVal():
            # Player 2 Wins
            print(f"{pl2.name} won the round!!")
            pl2.addCardPile(pl1CardList)
            pl2.addCardPile(pl2CardList)
        else:
            # War Happens
            print(f"It's a motherfucking war!")
            for x in range(2):
                # print(f"Player 1 Hand: {len(pl1.hand)}")
                # print(f"Player 1 Pile: {len(pl1.pile)}")
                # print(f"Player 2 Hand: {len(pl2.hand)}")
                # print(f"Player 2 Pile: {len(pl2.pile)}")
                if pl1.cardCount() == 0 or pl2.cardCount() == 0:
                    return
                pl1.ensureHandFull()
                pl2.ensureHandFull()
                pl1CardList.append(pl1.playCard())
                pl2CardList.append(pl2.playCard())
            Player.war(pl1, pl2, pl1CardList, pl2CardList)
        return