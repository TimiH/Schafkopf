from PIL import Image, ImageDraw, ImageFont
from GuiTools.handImage import handoToJpgStackedH, handToJpgV, handoToJpgStackedV, getCardImg, getHandArray
from helper import rotateListBackwards, sortHandByGameMode


def renderGameState(gameState, trickHistory, validCards=None, position=None):
    HEIGHT = 900
    WIDTH = 900
    PADDING = 25
    TRICKPADDING = 10
    COLOUR = (0, 153, 0, 0)
    SIZECARDH0 = (200, 340)  # before transform
    SIZECARD = (100, 170)  # after transform
    SIZEHAND = (450, 170)

    # hand Positions
    posN = (int(WIDTH / 2) - int(SIZEHAND[0] / 2), 0 + PADDING)
    posS = (int(WIDTH / 2) - int(SIZEHAND[0] / 2), HEIGHT - PADDING - SIZEHAND[1])
    posW = (0 + PADDING, int(HEIGHT / 2) - int(SIZEHAND[0] / 2))
    posE = (WIDTH - SIZEHAND[1] + PADDING, int(HEIGHT / 2) - int(SIZEHAND[0] / 2))

    # Main image
    img = Image.new('RGB', (WIDTH, HEIGHT), color=COLOUR)

    # Game state handling
    lead = gameState['leadingPlayer']
    # trickHistory = rotateListBackwards(trickHistory, lead)  # breaks if len<4? hack fill up with none
    gameMode = gameState['gameMode']

    # hands: ORDER 0123,SWNE
    handS = sortHandByGameMode(gameState['playersHands'][0], gameMode)
    handN = sortHandByGameMode(gameState['playersHands'][2], gameMode)
    handW = sortHandByGameMode(gameState['playersHands'][1], gameMode)
    handE = sortHandByGameMode(gameState['playersHands'][3], gameMode)
    handDict = {0: handS, 1: handW, 2: handN, 3: handE}
    # removing cards
    if trickHistory:
        for card in trickHistory:
            if card in handS:
                handS.remove(card)
            if card in handN:
                handN.remove(card)
            if card in handW:
                handW.remove(card)
            if card in handE:
                handE.remove(card)

    # greyscale non valid cards
    validIndex = []
    if validCards:
        currentPos = (len(trickHistory) + gameState['leadingPlayer']) % 4
        # currentPos = len(trickHistory)
        for card in validCards:
            validIndex.append(handDict[currentPos].index(card))
    currentPos = (len(trickHistory) + lead) % 4

    # handImages
    handS = getHandArray(handS)
    handN = getHandArray(handN)
    handW = getHandArray(handW)
    handE = getHandArray(handE)

    # Pasting hands to image
    for key, card in enumerate(handS):
        card.thumbnail(SIZECARD)
        if currentPos == 0 and key not in validIndex:
            card = card.convert('LA')
        pos = (posS[0] + key * int(SIZECARD[0] / 2), posS[1])
        img.paste(card, pos)
    for key, card in enumerate(handN):
        card.thumbnail(SIZECARD)
        if currentPos == 2 and key not in validIndex:
            card = card.convert('LA')
        pos = (posN[0] + key * int(SIZECARD[0] / 2), posN[1])
        img.paste(card, pos)
    for key, card in enumerate(handW):
        card.thumbnail(SIZECARD)
        if currentPos == 1 and key not in validIndex:
            card = card.convert('LA')
        # card = card.transpose(Image.ROTATE_90)
        pos = (posW[0], posW[1] + key * int(SIZECARD[0] / 2))
        img.paste(card, pos)
    for key, card in enumerate(handE):
        card.thumbnail(SIZECARD)
        if currentPos == 3 and key not in validIndex:
            card = card.convert('LA')
        # card = card.transpose(Image.ROTATE_90)
        pos = (posE[0], posE[1] + key * int(SIZECARD[0] / 2))
        img.paste(card, pos)

    # trickHistory
    # cardPositions
    cardN = (int(WIDTH / 2) - int(SIZECARD[0] / 2), int(HEIGHT / 2) - int(SIZECARD[1]) - TRICKPADDING)
    cardS = (int(WIDTH / 2) - int(SIZECARD[0] / 2), int(HEIGHT / 2) + +TRICKPADDING)
    cardW = (int(WIDTH / 2) - int(SIZECARD[1]) - TRICKPADDING, int(HEIGHT / 2) - int(SIZECARD[1] / 2))
    cardE = (int(WIDTH / 2) + int(SIZECARD[1]) + TRICKPADDING, int(HEIGHT / 2) - int(SIZECARD[1] / 2))

    cardPos = rotateListBackwards([cardS, cardW, cardN, cardW], gameState['leadingPlayer'])
    for key, card in enumerate(trickHistory):
        image = getCardImg(card)
        image.thumbnail(SIZECARD)
        img.paste(image, cardPos[key])

    # Draw Text
    # -----------------------
    draw = ImageDraw.Draw(img)
    fontSize = 40
    font = ImageFont.truetype('/home/tim/Work/Schafkopf/GuiTools/font/Russo Sans Bold.otf', fontSize)

    # playerNames
    NAMESPADDING = 20
    tPosS = (int(WIDTH / 2) - fontSize / 2, HEIGHT - SIZECARD[1] - NAMESPADDING - fontSize - 10)
    tPosE = (WIDTH - SIZECARD[0] - PADDING - fontSize - 10, int(HEIGHT / 2))
    tPosN = (int(WIDTH / 2) - fontSize / 2, SIZECARD[1] + NAMESPADDING)
    tPosW = (SIZECARD[0] + PADDING, int(HEIGHT / 2))
    draw.text(tPosS, 'S', font=font)
    draw.text(tPosW, 'W', font=font)
    draw.text(tPosN, 'N', font=font)
    draw.text(tPosE, 'E', font=font)
    # Rectangle
    rectPos0 = (WIDTH / 2 + SIZEHAND[0] / 2, PADDING)
    rectPos1 = (WIDTH - PADDING + 20, SIZECARD[1] + PADDING + 10)
    draw.rectangle((rectPos0, rectPos1), outline='black')
    # GameMode
    dictMode = {1: 'TEAM', 2: 'WENZ', 3: 'SOLO'}
    dictColor = {None: 'NONE', 0: 'EICHEL', 1: 'GRAS', 2: 'HERZ', 3: 'SCHELLEN'}
    gameText = dictMode[gameMode[0]] + ', ' + dictColor[gameMode[1]]
    # Scores
    scores = gameState['scores']
    scoresText = '\nS:' + str(scores[0]) + '\nW:' + str(scores[1]) + '\nN:' + str(scores[2]) + '\nE:' + str(scores[3])
    # Teams
    offensivePlayers = gameState['offensivePlayers']
    teamArr = ['S', 'W', 'N', 'E']
    offensiveTeam = [teamArr[x] for x in offensivePlayers]
    oppTeam = [teamArr[x] for x in range(4) if teamArr[x] not in offensiveTeam]
    teamText = '\nOFFENSIVE: \t' + str(offensiveTeam) + '\nOpposition:\t' + str(oppTeam)
    # searched and run away
    searchText = '\nSearched = ' + str(gameState['searched'])
    ranAwayText = '\nRan Away = ' + str(gameState['ranAway'])

    # Drawing gameState
    fontSize = 15
    font = ImageFont.truetype('/home/tim/Work/Schafkopf/GuiTools/font/Russo Sans Bold.otf', fontSize)
    draw.text((rectPos0[0] + 3, rectPos0[1] + 3), gameText + scoresText + teamText + searchText + ranAwayText,
              font=font)

    return img
