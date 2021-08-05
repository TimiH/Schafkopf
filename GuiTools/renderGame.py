from PIL import Image
from GuiTools.handImage import handoToJpgStackedH, handToJpgV, handoToJpgStackedV, getCardImg, getHandArray
from helper import rotateListBackwards


def renderGameState(gameState, trickHistory):
    HEIGHT = 900
    WIDTH = 900
    PADDING = 25
    TRICKPADDING = 10
    COLOUR = (0, 153, 0, 0)
    SIZECARD0 = (200, 340)  # before transform
    SIZECARD = (100, 170)  # after transform
    SIZEHAND = (450, 170)

    # hand Positions
    posN = (int(WIDTH / 2) - int(SIZEHAND[0] / 2), 0 + PADDING)
    posS = (int(WIDTH / 2) - int(SIZEHAND[0] / 2), HEIGHT - PADDING - SIZEHAND[1])
    # TODO flip
    # posW = (0 + PADDING, int(HEIGHT / 2) - int(SIZEHAND[0] / 2))
    # posE = (WIDTH - SIZEHAND[1] - PADDING, int(HEIGHT / 2) - int(SIZEHAND[0] / 2))

    # cardPositions
    cardN = (int(WIDTH / 2) - int(SIZECARD[0] / 2), int(HEIGHT / 2) - int(SIZECARD[1]) - TRICKPADDING)
    cardS = (int(WIDTH / 2) - int(SIZECARD[0] / 2), int(HEIGHT / 2) + +TRICKPADDING)

    cardW = (int(WIDTH / 2) - int(SIZECARD[1]) - TRICKPADDING, int(HEIGHT / 2) - int(SIZECARD[1] / 2))
    cardE = (int(WIDTH / 2) + int(SIZECARD[1]) + TRICKPADDING, int(HEIGHT / 2) - int(SIZECARD[1] / 2))
    cardPos = [cardS, cardW, cardN, cardW]

    img = Image.new('RGB', (WIDTH, HEIGHT), color=COLOUR)
    # handImages
    # #TODO handSortingByGameMode,removing played cards
    handS = getHandArray(gameState['playersHands'][0])
    handN = getHandArray(gameState['playersHands'][2])
    handW = getHandArray(gameState['playersHands'][1])
    handE = getHandArray(gameState['playersHands'][3])

    # Pasting hands to image
    for key, card in enumerate(handS):
        card.thumbnail(SIZECARD)
        pos = (posS[0] + key * int(SIZECARD[0] / 2), posS[1])
        img.paste(card, pos)
    for key, card in enumerate(handN):
        card.thumbnail(SIZECARD)
        pos = (posN[0] + key * int(SIZECARD[0] / 2), posN[1])
        img.paste(card, pos)
    for key, card in enumerate(handW):
        card.thumbnail(SIZECARD)
        card = card.transpose(Image.ROTATE_90)
        pos = (posW[0], posW[1] + key * int(SIZECARD[0] / 2))
        img.paste(card, pos)
    for key, card in enumerate(handE):
        card.thumbnail(SIZECARD)
        card = card.transpose(Image.ROTATE_90)
        pos = (posE[0], posE[1] + key * int(SIZECARD[0] / 2))
        img.paste(card, pos)

    # cards on the table
    lead = gameState['leadingPlayer']
    trickHistory = rotateListBackwards(trickHistory, lead)

    for key, card in enumerate(trickHistory):
        image = getCardImg(card)
        image.thumbnail(SIZECARD)
        img.paste(image, cardPos[key])

    return img
