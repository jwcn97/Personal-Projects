import pandas as pd
import numpy as np
import copy
from util import *

deck = {
    '2': 24,
    '3': 24,
    '4': 24,
    '5': 24,
    '6': 24,
    '7': 24,
    '8': 24,
    '9': 24,
    'T': 96,
    'A': 24
}

hands = list(deck.keys())

table2, table3, table4, table5 = [], [], [], []

tempPlayer = '22'
tempDealer = '2'
tempProb = 0

def getProb(tbl, phands):
    return tbl[tbl['playerHands'].apply(lambda x: x[0:2] == phands)].sum().probability

def decision(playerHands, dealerHands):
    global table2, table3, table4, table5

    prob5 = table5[((table5['playerHands'].apply(lambda x: x[0:2] == playerHands)) & (table5['dealerHands'].apply(lambda x: x == dealerHands)))].sum().probability
    prob4 = table4[((table4['playerHands'].apply(lambda x: x[0:2] == playerHands)) & (table4['dealerHands'].apply(lambda x: x == dealerHands)))].sum().probability
    prob3 = table3[((table3['playerHands'].apply(lambda x: x[0:2] == playerHands)) & (table3['dealerHands'].apply(lambda x: x == dealerHands)))].sum().probability
    prob2 = table2[((table2['playerHands'].apply(lambda x: x == playerHands)) & (table2['dealerHands'].apply(lambda x: x == dealerHands)))].sum().probability

    prob5 = round(prob5, 6)
    prob4 = round(prob4, 6)
    prob3 = round(prob3, 6)
    prob2 = round(prob2, 6)

    print(playerHands, dealerHands, prob2, prob3, prob4, prob5)
    probs = str(prob2) + ' ' + str(prob3) + ' ' + str(prob4) + ' ' + str(prob5)
    
    if prob3 >= prob2:
        if prob3 >= prob2 + prob4 + prob5: return 'D ' + probs
        else: return 'H ' + probs
    else: return 'S ' + probs

def calculateProbability(card, temp_deck, probability):
    # calculate probability
    probability *= temp_deck[card] / sum(temp_deck.values())
    # remove card from deck
    temp_deck[card] -= 1

    return temp_deck, probability

def stopDealer(playerCards, playerTotal, dealerCards, dealerTotal):
    # dealer stops taking
    if dealerTotal >= 17:
        # only print if player wins / draws
        if ((dealerTotal > 21) or (playerTotal >= dealerTotal)):
            # if dealer has a natural blackjack and player does not
            if ((dealerCards in ['AT','TA']) and (len(playerCards) > 2)): return True

            # copy deck into a temporary deck
            temp_deck = copy.deepcopy(deck)
            # set probability to 1
            probability = 1

            # remove player and dealer hands from the deck
            temp_deck[playerCards[0]] -= 1
            temp_deck[dealerCards[0]] -= 1
            temp_deck[playerCards[1]] -= 1

            # calculate probability for player and dealer draws
            for c in playerCards[2:]+dealerCards[1:]:
                temp_deck, probability = calculateProbability(c, temp_deck, probability)

            global tempPlayer, tempDealer, tempProb

            if ((tempDealer == None) or (dealerCards[0] != tempDealer)):
                if dealerCards[0] != tempDealer:
                    print(tempPlayer, tempDealer, tempProb)
                    if len(tempPlayer) == 2:
                        table2.append([tempPlayer, tempDealer, tempProb])
                    elif len(tempPlayer) == 3:
                        table3.append([tempPlayer, tempDealer, tempProb])
                    elif len(tempPlayer) == 4:
                        table4.append([tempPlayer, tempDealer, tempProb])
                    elif len(tempPlayer) == 5:
                        table5.append([tempPlayer, tempDealer, tempProb])

                tempDealer = dealerCards[0]
                tempPlayer = playerCards
                tempProb = probability
            elif dealerCards[0] == tempDealer:
                tempProb += probability

        return True

def dealerDraw(playerCards, playerTotal, dealer):
    for j in range(len(hands)):
        dealerCards = dealer + hands[j]
        dealerTotal = sum([getValue(i) for i in dealerCards])

        # change A to 1 if dealer busts
        if dealerTotal > 21:
            dealerTotal = handleAces(dealerCards, dealerTotal)

        # dealer hits required range, dealer stops drawing
        if stopDealer(playerCards, playerTotal, dealerCards, dealerTotal): continue
    
        # dealer hasn't hit required range, dealer continues drawing
        dealerDraw(playerCards, playerTotal, dealerCards)

for i in range(len(hands)):
    for j in range(i, len(hands)):
        cards = hands[i] + hands[j]
        total = sum([getValue(i) for i in cards])

        # blackjack
        if total == 21:
            dealerDraw(cards, total, hands[m])
            continue

        # bust
        if total > 21:
            total = handleAces(cards, total)
            if total > 21: continue
        # STAND
        for m in range(len(hands)):
            dealerDraw(cards, total, hands[m])

        # HIT
        for k in range(len(hands)):
            cards = hands[i] + hands[j] + hands[k]
            total = sum([getValue(i) for i in cards])

            # bust
            if total > 21:
                total = handleAces(cards, total)
                if total > 21: continue
            # STAND
            for m in range(len(hands)):
                dealerDraw(cards, total, hands[m])

            # HIT
            for l in range(len(hands)):
                cards = hands[i] + hands[j] + hands[k] + hands[l]
                total = sum([getValue(i) for i in cards])

                # bust
                if total > 21:
                    total = handleAces(cards, total)
                    if total > 21: continue
                # STAND
                for m in range(len(hands)):
                    dealerDraw(cards, total, hands[m])

                # HIT
                for n in range(len(hands)):
                    cards = hands[i] + hands[j] + hands[k] + hands[l] + hands[n]
                    total = sum([getValue(i) for i in cards])

                    # bust
                    if total > 21:
                        total = handleAces(cards, total)
                        if total > 21: continue
                    # STAND
                    for m in range(len(hands)):
                        dealerDraw(cards, total, hands[m])

print(tempPlayer, tempDealer, tempProb)
if len(tempPlayer) == 2:
    table2.append([tempPlayer, tempDealer, tempProb])
elif len(tempPlayer) == 3:
    table3.append([tempPlayer, tempDealer, tempProb])
elif len(tempPlayer) == 4:
    table4.append([tempPlayer, tempDealer, tempProb])
elif len(tempPlayer) == 5:
    table5.append([tempPlayer, tempDealer, tempProb])

table2 = pd.DataFrame(table2, columns=['playerHands', 'dealerHands', 'probability'])
table3 = pd.DataFrame(table3, columns=['playerHands', 'dealerHands', 'probability'])
table4 = pd.DataFrame(table4, columns=['playerHands', 'dealerHands', 'probability'])
table5 = pd.DataFrame(table5, columns=['playerHands', 'dealerHands', 'probability'])

# table2.to_excel('test2.xlsx')
# table3.to_excel('test3.xlsx')
# table4.to_excel('test4.xlsx')
# table5.to_excel('test5.xlsx')

# table = []
# for i in range(len(hands)):
#     for j in range(i, len(hands)):
#         for k in range(len(hands)):
#             table.append([hands[i]+hands[j], hands[k], decision(hands[i]+hands[j], hands[k])])
            
# table = pd.DataFrame(table, columns=['playerHands', 'dealerHand', 'decision'])
# table = table.set_index(['playerHands','dealerHand'])
# table = table.T.stack().T
# table.to_excel('table_test.xlsx')