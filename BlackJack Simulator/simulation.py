import pandas as pd
import numpy as np
from util import *

def dealerDraw(dealerCards, deck):
    dealerTotal = 0
    while dealerTotal < 17:
        card, deck = deal(deck)
        dealerCards += card
        dealerTotal = getTotal(dealerCards)

    return dealerCards, deck

def playerDraw(playerCards, dealerCards, deck):
    # bet multiplier
    multiplier = 1
    split = False

    # blackjack
    if playerCards in ['AT','TA']:
        return playerCards, deck, multiplier, split

    # draw cards
    while True:
        decision = handleAction(playerCards, dealerCards)
        if decision == 'S': return playerCards, deck, multiplier, split

        # hit or double
        if decision != 'SP':
            card, deck = deal(deck)
            playerCards += card

            if decision == 'D':
                multiplier = 2
                return playerCards, deck, multiplier, split

        # split
        else:
            split = True
            return playerCards, deck, multiplier, split
        
        if getTotal(playerCards) > 21: return playerCards, deck, multiplier, split

def handleAction(playerCards, dealerCards):
    if dealerCards == 'A': dealer = 9
    elif dealerCards == 'T': dealer = 8
    else: dealer = int(dealerCards) - 2

    playerTotal = getTotal(playerCards)

    if len(playerCards) == 2:
        if playerCards[0] == playerCards[1]:
            action = table[playerCards][dealer]
        elif 'A' in playerCards:
        # if 'A' in playerCards:
            action = table['A'+sorted(playerCards)[0]][dealer]
        else:
            action = table[str(playerTotal)][dealer]
    else:
        if 'A' in playerCards:
            total = sum([getValue(i) for i in playerCards])-11
            if total > 9: action = table[str(playerTotal)][dealer]
            else:         action = table['A'+str(total)][dealer]
        else:
            action = table[str(playerTotal)][dealer]

    if type(action) == type([]):
        rc, tc = count(deck)
        action = action[2] if tc >= action[1] else action[0]

    return action

def playerTurn(playerCards, dealerCards, bet, totalSets, deck):
    playerCards, deck, multiplier, split = playerDraw(playerCards, dealerCards, deck)

    if split:
        c1, deck = deal(deck)
        c2, deck = deal(deck)
        p1, deck, m1, s1 = playerDraw(playerCards[0]+c1, dealerCards, deck)
        p2, deck, m2, s2 = playerDraw(playerCards[1]+c2, dealerCards, deck)

        totalSets.append({ 'player': p1, 'bet': bet*m1 })
        totalSets.append({ 'player': p2, 'bet': bet*m2 })
    else:
        totalSets.append({ 'player': playerCards, 'bet': bet*multiplier })

    return totalSets, deck

################################ SIMULATION ################################

lifetime = []
mainBet = 15
numPlayers = 3
playerPosition = 1

suites, decks = 4, 6
numGames = 25    # number of games to be played for each 6-deck game
totalGames = 40  # number of 6-deck games to be played

for j in range(totalGames):
    winnings = []

    deck = {
        '2': suites*decks, '3': suites*decks, '4': suites*decks, '5': suites*decks, '6': suites*decks,
        '7': suites*decks, '8': suites*decks, '9': suites*decks,
        'T': suites*decks, 'J': suites*decks, 'Q': suites*decks, 'K': suites*decks, 'A': suites*decks
    }

    hands = list(deck.keys())

    # start of simulation
    for i in range(numGames):
        totalSets = []
        card1 = ''

        # place bets
        rc, tc = count(deck)
        numCards = totalInDeck(deck)

        if tc > 0:
            bet = mainBet * (tc-1)
        else:
            bet = mainBet

        for j in range(numPlayers):
            # deal 1st cards for all players
            card, deck = deal(deck)
            card1 += card

        # deal dealer's card
        dealerCards, deck = deal(deck)

        for j in range(numPlayers):
            # deal 2nd card for each player
            card, deck = deal(deck)

            # player turn
            if j != playerPosition:
                totalSets, deck = playerTurn(card1[j]+card, dealerCards, 0, totalSets, deck)
            else:
                totalSets, deck = playerTurn(card1[j]+card, dealerCards, bet, totalSets, deck)

        # dealer draws and decide winners
        dealerCards, deck = dealerDraw(dealerCards, deck)
        result = decideWinner(totalSets, dealerCards)
        winnings.append(result)
        
    if sum(winnings) != 0: print(winnings)
    lifetime.append(sum(winnings))

test = [i for i in lifetime if i != 0]
print('lifetime:',test,sum(lifetime))