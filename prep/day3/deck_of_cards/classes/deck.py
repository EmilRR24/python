from .card import Card
import random

class Deck:
    def __init__( self ):
        suits = [ "spades" , "hearts" , "clubs" , "diamonds" ]
        self.cards = []

        for s in suits:
            for i in range(1,14):
                str_val = ""
                if i == 1:
                    str_val = "Ace"
                elif i == 11:
                    str_val = "Jack"
                elif i == 12:
                    str_val = "Queen"
                elif i == 13:
                    str_val = "King"
                else:
                    str_val = str(i)
                self.cards.append( Card( s , i , str_val ) )

    def distributeCards(self, playerClass):
        cardsPerPlayer = 26
        while self.cards:
            for pl in playerClass.players:
                pl.drawCard()
    def giveCard(self):
        cardInd = random.randint(0,len(self.cards)-1)
        return self.cards.pop(cardInd)
    def show_cards(self):
        for card in self.cards:
            print(card.card_info())