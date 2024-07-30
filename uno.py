#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 20:37:38 2024

@author: Watson
"""

import random
 
class UnoCard:
    '''represents an Uno card
    attributes:
      rank: int from 0 to 9
      color: string'''
 
    def __init__(self, rank, color, action="none"):
        '''UnoCard(rank, color) -> UnoCard
        creates an Uno card with the given rank and color'''
        self.rank = rank
        self.color = color
        self.action = action
        #... 10: skipUno; 11: reverseUno; 12: drawtwoUno; 13: wildUno; 14: drawfourUno
        if self.rank == 10:
            self.action = "skip"
        elif self.rank == 11:
            self.action = "reverse"
        elif self.rank == 12:
            self.action = "drawtwo"
        elif self.rank == 13:
            self.action = "wild"
        elif self.rank == 14:
             self.action = "drawfour"
             
    def __str__(self):
        '''str(Unocard) -> str'''
        if self.rank < 10:
            return(str(self.color) + ' ' + str(self.rank))
        #... 10: skipUno; 11: reverseUno; 12: drawtwoUno; 13: wildUno; 14: drawfourUno
        elif self.rank == 10:
            return(str(self.color) + ' Skip')
        elif self.rank == 11:
            return(str(self.color) + ' Reverse')
        elif self.rank == 12:
            return(str(self.color) + ' DrawTwo')
        elif self.rank == 13:
            return(str(self.color) + ' Wild')
        elif self.rank == 14:
            return(str(self.color) + ' Wild DrawFour')
        
    def is_match(self, other):
        '''UnoCard.is_match(UnoCard) -> boolean
        returns True if the cards match in rank or color, False if not'''
        ismatch = False
        #... match of normal cards
        if self.color == other.color or self.rank == other.rank:
            ismatch = True
        #... wild cards
        if self.color == "none":
            ismatch = True
        return ismatch
 
class UnoDeck:
    '''represents a deck of Uno cards
    attribute:
      deck: list of UnoCards'''
 
    def __init__(self):
        '''UnoDeck() -> UnoDeck
        creates a new full Uno deck'''
        self.deck = []
        for color in ['red', 'blue', 'green', 'yellow']:
            self.deck.append(UnoCard(0, color))  # one 0 of each color = 4
            for i in range(2):
                #... two of each of 1-9 of each color = 18 * 4 = 72
                #... two of each action card of each color, denoted as
                #... 10: skipUno; 11: reverseUno; 12: drawtwoUno = 3 * 2 * 4 = 24
                for n in range(1, 13):
                    self.deck.append(UnoCard(n, color))
        #... add four wild card
        color = 'none'
        for n in range(4):
            #... 20: wild card
            nrank = 13
            self.deck.append(UnoCard(nrank, color))
        #... add four wild drawfour
        for n in range(4):
            #... 20: wild card
            nrank = 14
            self.deck.append(UnoCard(nrank, color))
        #... check total number of cards
        #print("total cards = ", len(self.deck))
        random.shuffle(self.deck)  # shuffle the deck
 
    def __str__(self):
        '''str(Unodeck) -> str'''
        return 'An Uno deck with '+str(len(self.deck)) + ' cards remaining.'
 
    def is_empty(self):
        '''UnoDeck.is_empty() -> boolean
        returns True if the deck is empty, False otherwise'''
        #... print a message to tell when the deck is empty.
        #print("The deck is empty now. Cards in the pile are taken back to deck.")
        return len(self.deck) == 0
 
    def deal_card(self):
        '''UnoDeck.deal_card() -> UnoCard
        deals a card from the deck and returns it
        (the dealt card is removed from the deck)'''
        return self.deck.pop()
 
    def reset_deck(self, pile):
        '''UnoDeck.reset_deck(pile) -> None
        resets the deck from the pile'''
        if len(self.deck) != 0:
            return
        self.deck = pile.reset_pile() # get cards from the pile
        random.shuffle(self.deck)  # shuffle the deck
 
class UnoPile:
    '''represents the discard pile in Uno
    attribute:
      pile: list of UnoCards'''
 
    def __init__(self, deck):
        '''UnoPile(deck) -> UnoPile
        creates a new pile by drawing a card from the deck'''
        card = deck.deal_card()
        while card.color == "none":
            card = deck.deal_card()
        #... initialize the pile list by dealing one card from the deck
        #... if the initial top is a wild card, deal another one from the deck
        self.pile = [card]
 
    def __str__(self):
        '''str(UnoPile) -> str'''
        return 'The pile has ' + str(self.pile[-1]) + ' on top.'
 
    def top_card(self):
        '''UnoPile.top_card() -> UnoCard
        returns the top card in the pile'''
        return self.pile[-1]
 
    def add_card(self, card):
        '''UnoPile.add_card(card) -> None
        adds the card to the top of the pile'''
        self.pile.append(card)
        
    def check_action(self):
        return self.top_card().action
    
    def remove_action(self):
        self.top_card().action = "none"
        return self.top_card().action
 
    def reset_pile(self):
        '''UnoPile.reset_pile() -> list
        removes all but the top card from the pile and
          returns the rest of the cards as a list of UnoCards'''
        newdeck = self.pile[:-1]
        self.pile = [self.pile[-1]]
        return newdeck
 
class UnoPlayer:
    '''represents a player of Uno
    attributes:
      name: a string with the player's name
      hand: a list of UnoCards'''
 
    def __init__(self, name, deck):
        '''UnoPlayer(name, deck) -> UnoPlayer
        creates a new player with a new 7-card hand'''
        self.name = name
        self.hand = [deck.deal_card() for i in range(7)]
 
    def __str__(self):
        '''str(UnoPlayer) -> UnoPlayer'''
        return str(self.name) + ' has ' + str(len(self.hand)) + ' cards.'
 
    def get_name(self):
        '''UnoPlayer.get_name() -> str
        returns the player's name'''
        return self.name
 
    def get_hand(self):
        '''get_hand(self) -> str
        returns a string representation of the hand, one card per line'''
        output = ''
        for card in self.hand:
            output += str(card) + '\n'
        return output
 
    def has_won(self):
        '''UnoPlayer.has_won() -> boolean
        returns True if the player's hand is empty (player has won)'''
        return len(self.hand) == 0
 
    def draw_card(self, deck):
        '''UnoPlayer.draw_card(deck) -> UnoCard
        draws a card, adds to the player's hand
          and returns the card drawn'''
        card = deck.deal_card()  # get card from the deck
        self.hand.append(card)   # add this card to the hand
        return card
 
    def play_card(self, card, pile):
        '''UnoPlayer.play_card(card, pile) -> None
        plays a card from the player's hand to the pile
        CAUTION: does not check if the play is legal!'''
        self.hand.remove(card)
        pile.add_card(card)
        if card.color == "none":
            #... pick a color for the wild card
            icolor = ['red', 'blue', 'green', 'yellow']
            for index in range(4):
                # print the color to be assigned to the wild card
                print(str(index + 1) + ": " + str(icolor[index]))
            # get player's choice of which color to assign
            choice = 0
            while choice < 1 or choice > len(icolor):
                choicestr = input("What color do you want for the wild card? ")
                if choicestr.isdigit():
                    choice = int(choicestr)
            # assign the chosen color to the wild card
            card.color = icolor[choice - 1]
        print(pile)

    def take_turn(self, deck, pile):
        '''UnoPlayer.take_turn(deck, pile) -> None
        takes the player's turn in the game
          deck is an UnoDeck representing the current deck
          pile is an UnoPile representing the discard pile'''
        
        # print player info
        print(self.name + ", it's your turn.")
        print(pile)
        print("Your hand: ")
        print(self.get_hand())
        # get a list of cards that can be played
        topcard = pile.top_card()
        matches = [card for card in self.hand if card.is_match(topcard)]
        
        #... can play
        if len(matches) > 0:
            for index in range(len(matches)):
                # print the playable cards with their number
                print(str(index + 1) + ": " + str(matches[index]))
            # get player's choice of which card to play
            choice = 0
            while choice < 1 or choice > len(matches):
                choicestr = input("Which do you want to play? ")
                if choicestr.isdigit():
                    choice = int(choicestr)
            # play the chosen card from hand, add it to the pile
            self.play_card(matches[choice - 1], pile)
            
        #... can't play
        else:
            print("You can't play, so you have to draw.")
            input("Press enter to draw.")
            
            # check if deck is empty -- if so, reset it
            if deck.is_empty():
                deck.reset_deck(pile)
            
            # draw a new card from the deck
            newcard = self.draw_card(deck)
            print("You drew: "+str(newcard))
            if newcard.is_match(topcard): # can be played
                print("Good -- you can play that!")
                self.play_card(newcard,pile)
            
            #... still can't play   
            else:
                print("Sorry, you still can't play.")
            
            input("Press enter to continue.")

class UnoComputer(UnoPlayer):
    '''represents a computer player of Uno
    attributes:
      name: a string with the player's name
      hand: a list of UnoCards
      aiLevel: an int of how smart it is. It has three levels'''
    
    def __init__(self, name, deck, aiLevel):
        UnoPlayer.__init__(self, name, deck)
        self.aiLevel = aiLevel
    
    def take_turn(self, deck, pile):
        '''UnoComputer.take_turn(deck, pile) -> None
        takes the Computer's turn in the game
          deck is an UnoDeck representing the current deck
          pile is an UnoPile representing the discard pile'''
        
        # print player info
        print(self.name + ", it's your turn.")
        print(pile)
        print("Your hand: ")
        print(self.get_hand())
        # get a list of cards that can be played
        topcard = pile.top_card()
        matches = [card for card in self.hand if card.is_match(topcard)]
        
        #... can play
        if len(matches) > 0:
            for index in range(len(matches)):
                # print the playable cards with their number
                print(str(index + 1) + ": " + str(matches[index]))
                
            # computer's choice of which card to play
            if self.aiLevel == "First Choice mode":
                choice = 1
            elif self.aiLevel == "Action mode":
                #... find the action card, if more than 1 action card, choose the first
                for card in matches:
                    if card.action != "none":
                        choice = matches.index(card)
                    else:
                        choice = random.randrange(1, len(matches) + 1)
            elif self.aiLevel == "Random mode":
                choice = random.randrange(1, len(matches) + 1)
                
            # print([card.action for card in matches])
            
            # play the chosen card from hand, add it to the pile
            self.play_card(matches[choice - 1], pile)
            
        #... can't play
        else:
            print("You can't play, so you have to draw.")
            #input("Press enter to draw.")
            
            # check if deck is empty -- if so, reset it
            if deck.is_empty():
                deck.reset_deck(pile)
            
            # draw a new card from the deck
            newcard = self.draw_card(deck)
            print("You drew: "+str(newcard))
            if newcard.is_match(topcard): # can be played
                print("Good -- you can play that!")
                self.play_card(newcard,pile)
            
            #... still can't play   
            else:
                print("Sorry, you still can't play.")
            
            #input("Press enter to continue.")
        
    def play_card(self, card, pile):
        '''UnoPComputer.play_card(card, pile) -> None
        plays a card from the player's hand to the pile
        CAUTION: does not check if the play is legal!'''
        self.hand.remove(card)
        pile.add_card(card)
        if card.color == "none":
            #... computer's choice to pick color for the wild card
            icolor = ['red', 'blue', 'green', 'yellow']
            for index in range(4):
                # print the color to be assigned to the wild card
                print(str(index + 1) + ": " + str(icolor[index]))
            # get player's choice of which color to assign
            if self.aiLevel == "First Choice mode":
                choice = 1
            elif self.aiLevel == "Action mode":
                choice = random.randrange(1, len(icolor) + 1)
            elif self.aiLevel == "Random mode":
                choice = random.randrange(1, len(icolor) + 1)
            # assign the chosen color to the wild card
            card.color = icolor[choice - 1]
        print(pile)
    
#... set up the game to include computer players and/or human players
def set_up_game(deck):
    '''set_up_game() -> (list, list)
    returns a list of players' names and a list
    of whether the player is a computer'''
    
    numPlayers = ''
    
    while not numPlayers.isdigit():
        numPlayers = input("How many people are playing UNO? ")
    numPlayers = int(numPlayers)

    # initialize list of players
    playerList = []
    
    # get player data
    for n in range(numPlayers):
        computerPlayer = ''
        while not (computerPlayer == 'y' or computerPlayer == 'n'):
            computerPlayer = input("Player " + str(n + 1) + ": Is this player a computer (y/n): ")
        isComputer = (computerPlayer == 'y')
        if isComputer:
            #... get the name for the computer player
            name = input("Enter the name of computer: ")
            computername = 'Computer' + name
            #... pick a level for the computer player
            ilevel = ['First Choice mode', 'Action mode', 'Random mode']
            for index in range(len(ilevel)):
                # print the color to be assigned to the wild card
                print(str(index + 1) + ": " + str(ilevel[index]))
            #... set up the AI level for the computer player
            choice = 0
            while choice < 1 or choice > len(ilevel):
                choicestr = input("What AI level is this computer? ")
                if choicestr.isdigit():
                    choice = int(choicestr)
            # assign the chosen AI level to the computer
            playerList.append(UnoComputer(computername, deck, ilevel[choice - 1]))
            
        else:
            name = input("Enter your name: ")
            playerList.append(UnoPlayer(name, deck))
    
    return playerList

def play_uno():
    '''play_uno(numPlayers) -> None
    plays a game of Uno with numPlayers'''
    
    # set up full deck and initial discard pile
    deck = UnoDeck()
    pile = UnoPile(deck)
    
    # set up the players, get players' names and types
    playerList = set_up_game(deck)
    #... number of players
    numPlayers = len(playerList)
  
    # randomly assign who goes first
    currentPlayerNum = random.randrange(numPlayers)
    
    #... print to verify
    #print([player.name for player in playerList])

    # play the game
    while True:
        
        # print the game status
        print('-------')
        for player in playerList:
            print(player)
        print('-------')

        #... check action card
        action = pile.check_action()
        
        #... check if the player is a computer player
        if "Computer" in playerList[currentPlayerNum].name:
            iscomputer = True
        else:
            iscomputer = False
    
        #... action card: skip
        if action == "skip":
            player = playerList[currentPlayerNum]
            print(player.name + ", it's your turn.")
            print("Sorry, your turn was skipped! Better luck next time!")
            if not iscomputer:
                input("Press enter to continue.")
            #... the action is only applied once
            pile.remove_action()
            #... go to the next player
            currentPlayerNum = (currentPlayerNum + 1) % numPlayers

        #... action card:reverse
        elif action == "reverse":
            #... return to the player who has just played before reverse
            justPlayerNum = (currentPlayerNum + numPlayers - 1) % numPlayers
            justPlayer = playerList[justPlayerNum]
            #... A print out message to tell the "reverse"
            print("The reverse card has been played so the playing order has to be reversed.")
            #... reverse the player list
            playerList.reverse()
            #... this is a print out to test if the player list has been reversed successfully
            #print("play list after reverse:", [player.name for player in playerList])
            #... the action is only applied once
            pile.remove_action()
            #... make a dictionary to map the player name with the list index after reverse
            listInd = list(range(numPlayers))
            listPlayername = [player.name for player in playerList]
            playerDict = dict(zip(listPlayername, listInd))
            
            #... reset current player after reverse
            currentPlayerNum = (playerDict[justPlayer.name] + 1) % numPlayers
            if "Computer" in playerList[currentPlayerNum].name:
                iscomputer = True
            else:
                iscomputer = False
                
            # take a turn
            playerList[currentPlayerNum].take_turn(deck, pile)
            # check for a winner
            if playerList[currentPlayerNum].has_won():
                print(playerList[currentPlayerNum].get_name() + " wins!")
                print("Thanks for playing!")
                break
            # go to the next player
            currentPlayerNum = (currentPlayerNum + 1) % numPlayers
        
        #... action card: drawtwo
        elif action == "drawtwo":
            #... check the current player
            player = playerList[currentPlayerNum]
            print(player.name + ", it's your turn.")
            print("Sorry, you have to draw two cards and you can't play because a DrawTwo card has been played.")
            if not iscomputer:
                input("Press enter to continue.")
            #... draw two cards
            playerList[currentPlayerNum].draw_card(deck)
            playerList[currentPlayerNum].draw_card(deck)
            #... the action is only applied once
            pile.remove_action()
            #... go to the next player
            currentPlayerNum = (currentPlayerNum + 1) % numPlayers
        
        #... action card: drawfour
        elif action == "drawfour":
            #... check the current player
            player = playerList[currentPlayerNum]
            print(player.name + ", it's your turn.")
            print("Sorry, you have to draw four cards and you can't play because a Wild DrawFour card has been played.")
            if not iscomputer:
                input("Press enter to continue.")
            #... draw four cards
            playerList[currentPlayerNum].draw_card(deck)
            playerList[currentPlayerNum].draw_card(deck)
            playerList[currentPlayerNum].draw_card(deck)
            playerList[currentPlayerNum].draw_card(deck)
            #... the action is only applied once
            pile.remove_action()
            #... go to the next player
            currentPlayerNum = (currentPlayerNum + 1) % numPlayers
            
        else:
            # take a turn
            playerList[currentPlayerNum].take_turn(deck, pile)
            # check for a winner
            if playerList[currentPlayerNum].has_won():
                print(playerList[currentPlayerNum].get_name() + " wins!")
                print("Thanks for playing!")
                break
            # go to the next player
            currentPlayerNum = (currentPlayerNum + 1) % numPlayers
    
#... call to play
play_uno()
