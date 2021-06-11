from PIL import Image
from helper import sortHand, sortHandByGameMode

path = '/home/tim/Work/Schafkopf/GuiTools/cardImages/'


def getCardImg(card):
    name = card.__repr__() + '.jpg'
    image = Image.open(path + name)
    return image


def handoToJpgStacked(hand):
    if not hand:
        return None
    images = []
    for card in hand:
        img = getCardImg(card)
        images.append(img)

    height = images[0].height
    width = images[0].width
    numImg = len(hand)

    new = Image.new('RGB', (int(width * 0.5) + int(width * (numImg) * 0.5), height))
    new.paste(images[0], (0, 0))
    # new.show()
    for key, img in enumerate(images[1::]):
        new.paste(img, (int((key + 1) * width * 0.5), 0))
        # new.show()
    return new


def handToJpg(hand):
    if not hand:
        return None
    images = []
    for card in hand:
        img = getCardImg(card)
        images.append(img)

    height = images[0].height
    width = images[0].width
    numImg = len(hand)

    new = Image.new('RGB', (width * numImg, height))
    for key, img in enumerate(images):
        new.paste(img, (key * width, 0))
    return new


from Deck import Deck

d = Deck()
d.shuffle()
hand = d.deal(8)
gameMode = (1, 2)
hand = sortHandByGameMode(hand, gameMode)
# handjpg = handToJpg(hand)
handjpg = handoToJpgStacked(hand)
# handjpg.show()
handjpg.save('handexample.jpg')
