from GameModes import MODES
from CardValues import SUITS, RANKS
from Card import Card
import random
from QstateHelper import createQstates, convertBitArraysInDictTo01
import json
import pickle
import uuid
import os


class Player(object):
    def __init__(self, name, record=False, targetFile=''):
        self.name = name
        self.hand = []
        self.position = None
        self.record = record
        self.states = {}
        self.target = targetFile

    ##TODO __repr__ and __str__

    def setHand(self, cards):
        self.hand = cards

    def setPosition(self, postion):
        self.position = postion

    def makeBid(self, validBids):
        # for bid in validBids:
        #     if bid[0] == 1:
        #         return bid
        # return (None,None)
        card = random.choice(validBids)
        return card

    def playCard(self, validCards, state, trickHistory):
        if not validCards:
            print((self.name, "STOP NO VALID CARDS with Hand:", self.hand))
        card = random.choice(validCards)

        return card

    def sortHand(self, state):
        pass

    def getPosition(self, gameDict):
        for key, value in enumerate(gameDict['players']):
            if value.name == self.name:
                return key

    def setResults(self, resultsDict):
        if self.record:
            for i in list(self.states.keys()):
                self.states[i].update(resultsDict)

    def recordQstate(self, hand, validCards, playedCard, gameDict, trickHistory):
        qstates = createQstates(hand, validCards, playedCard, self.position, gameDict, trickHistory)
        convertBitArraysInDictTo01(qstates)
        name = abs(len(hand) - 8)
        self.states['Round' + str(name)] = qstates

    def saveRecordsJson(self):
        if self.record:
            id = str(uuid.uuid4())
            records = {id: self.states}
            path = os.getcwd() + '/DataDump/json/' + id + '.json'
            with open(path, 'wb') as out:
                json.dump(records, out, sort_keys=True, indent=3)

    def saveRecordsPickle(self):
        id = str(uuid.uuid4()) + '.p'
        path = os.getcwd() + '/DataDump/pickle'
        with open(path + id, 'wb') as out:
            pickle.dump(self.record, out)
