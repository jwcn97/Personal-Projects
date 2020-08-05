import numpy as np

def handleAces(hand, total):
    occurrences = hand.count('A')
    for i in range(occurrences):
        total -= 10
        if total <= 21: return total
    return total

def getValue(card):
    if card == 'T':   return 10
    elif card == 'A': return 11
    else:             return int(card)

def getTotal(cards):
    total = sum([getValue(i) for i in cards])
    if total > 21: total = handleAces(cards, total)
    return total

def deal(deck):
    card = list(deck.keys())[np.random.randint(0,len(deck))]
    deck[card] -= 1
    if deck[card] == 0: del deck[card]
    if card in ['J','Q','K']: card = 'T'
    return card, deck

def totalInDeck(deck):
    totalCards = 0
    for card in deck:
        totalCards += deck[card]

    return totalCards

def count(deck):
    total = 0
    totalCards = 0
    for card in deck:
        totalCards += deck[card]
        if card in ['2','3','4','5','6']:   total -= deck[card]
        elif card in ['T','J','Q','K','A']: total += deck[card]

    halfDecks = round(totalCards/52 * 2) / 2
    if halfDecks == 0: halfDecks = 0.5
    return total, round(total/halfDecks)

def blackjack(cards):
    if cards in ['AT','TA']: return True
    return False

def decideWinner(totalSets, dealerCards):
    totalResult = 0
    dealerTotal = getTotal(dealerCards)

    for i in range(len(totalSets)):
        playerTotal = getTotal(totalSets[i]['player'])

        # player busts
        if playerTotal > 21: result = -1*totalSets[i]['bet']
        # player blackjack
        elif blackjack(totalSets[i]['player']): result = 0 if blackjack(dealerCards) else 1.5*totalSets[i]['bet']
        # player wins
        elif ((dealerTotal > 21) or (playerTotal > dealerTotal)): result = 1*totalSets[i]['bet']
        # player and dealer tie
        elif playerTotal == dealerTotal: result = -1*totalSets[i]['bet'] if blackjack(dealerCards) else 0
        # player loses to dealer
        else: result = -1*totalSets[i]['bet']
    
        totalResult += result

    return totalResult

# table = {
#     'AA': ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ],
#     'A9': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
#     'A8': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
#     'A7': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'H', 'S', 'S' ],
#     'A6': ['H', 'H', 'H', 'H', 'D', 'S', 'H', 'H', 'H', 'H' ],
#     'A5': ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ],
#     'A4': ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ],
#     'A3': ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ],
#     'A2': ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ],
#     '21': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
#     '20': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
#     '19': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
#     '18': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
#     '17': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
#     '16': ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H' ],
#     '15': ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H' ],
#     '14': ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H' ],
#     '13': ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H' ],
#     '12': ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ],
#     '11': ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H', 'H' ],
#     '10': ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H', 'H' ],
#     '9':  ['H', 'H', 'H', 'H', 'D', 'H', 'H', 'H', 'H', 'H' ],
#     '8':  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ],
#     '7':  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ],
#     '6':  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ],
#     '5':  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ],
#     '4':  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ]
# }


# table = {
#     'AA': ['SP','SP','SP','SP','SP','SP','SP','SP','SP','SP'],
#     'TT': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
#     '99': ['SP','SP','SP','SP','SP','S', 'SP','SP','S', 'S' ],
#     '88': ['SP','SP','SP','SP','SP','SP','SP','SP','SP','SP'],
#     '77': ['SP','SP','SP','SP','SP','SP','H', 'H', 'H', 'H' ],
#     '66': ['SP','SP','SP','SP','SP','H', 'H', 'H', 'H', 'H' ],
#     '55': ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H' ],
#     '44': ['H', 'H', 'H', 'SP','SP','H', 'H', 'H', 'H', 'H' ],
#     '33': ['SP','SP','SP','SP','SP','SP','H', 'H', 'H', 'H' ],
#     '22': ['SP','SP','SP','SP','SP','SP','H', 'H', 'H', 'H' ],
#     'A9': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
#     'A8': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
#     'A7': ['D', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H' ],
#     'A6': ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H' ],
#     'A5': ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H' ],
#     'A4': ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H' ],
#     'A3': ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H' ],
#     'A2': ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H' ],
#     '21': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
#     '20': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
#     '19': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
#     '18': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
#     '17': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
#     '16': ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H' ],
#     '15': ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H' ],
#     '14': ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H' ],
#     '13': ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H' ],
#     '12': ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H' ],
#     '11': ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H' ],
#     '10': ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H' ],
#     '9':  ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H' ],
#     '8':  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ],
#     '7':  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ],
#     '6':  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ],
#     '5':  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ]
# }

table = {
    'AA': ['SP','SP','SP','SP','SP','SP','SP','SP','SP','SP'],
    'TT': ['S', ['S',8,'SP'], ['S',6,'SP'], ['S',5,'SP'], ['S',4,'SP'], 'S', 'S', 'S', 'S', 'S' ],
    '99': ['SP','SP','SP','SP','SP','S', 'SP','SP','S', 'S' ],
    '88': ['SP','SP','SP','SP','SP','SP','SP','SP','SP','SP'],
    '77': ['SP','SP','SP','SP','SP','SP','H', 'H', 'H', 'H' ],
    '66': ['SP','SP','SP','SP','SP','H', 'H', 'H', 'H', 'H' ],
    '55': ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H' ],
    '44': ['H', 'H', 'H', 'SP','SP','H', 'H', 'H', 'H', 'H' ],
    '33': [['H',0,'SP'],'SP','SP','SP','SP','SP','H', 'H', 'H', 'H' ],
    '22': ['SP','SP','SP','SP','SP','SP','H', 'H', 'H', 'H' ],
    'A9': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
    'A8': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
    'A7': [['H',0,'D'], 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H' ],
    'A6': ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H' ],
    'A5': ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H' ],
    'A4': ['H', 'H', ['H',0,'D'], ['H',-4,'D'], 'D', 'H', 'H', 'H', 'H', 'H' ],
    'A3': ['H', 'H', 'H', ['H',-1,'D'], ['H',-4,'D'], 'H', 'H', 'H', 'H', 'H' ],
    'A2': ['H', 'H', 'H', ['H',0,'D'], ['H',-1,'D'], 'H', 'H', 'H', 'H', 'H' ],
    '21': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
    '20': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
    '19': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
    '18': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
    '17': ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S' ],
    '16': ['S', 'S', 'S', 'S', 'S', ['H',9,'S'], ['H',7,'S'], ['H',5,'S'], ['H',0,'S'], ['H',8,'S'] ],
    '15': ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H' ],
    '14': ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H' ],
    '13': [['H',0,'S'], ['H',-1,'S'], ['H',-3,'S'], ['H',-4,'S'], ['H',-4,'S'], 'H', 'H', 'H', 'H', 'H' ],
    '12': [['H',3,'S'], ['H',2,'S'], ['H',0,'S'], ['H',-1,'S'], ['H',0,'S'], 'H', 'H', 'H', 'H', 'H' ],
    '11': ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', ['H',1,'D'] ],
    '10': ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', ['H',4,'D'], ['H',4,'D'] ],
    '9':  [['H',1,'D'], ['H',0,'D'], ['H',-2,'D'], ['H',-4,'D'], ['H',-6,'D'], ['H',3,'D'], ['H',7,'D'], 'H', 'H', 'H' ],
    '8':  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ],
    '7':  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ],
    '6':  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ],
    '5':  ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H' ]
}