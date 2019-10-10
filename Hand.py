class Hand(object):
    hand = []

    #Contains a List of CARDS
    def __init__(self,cards):
        self.hand = cards

    def __str__(self):
        ret = ""
        for s in self.hand:
            ret += s.__str__()
            ret +=","
        return ret[-1]

#TODO sorting
