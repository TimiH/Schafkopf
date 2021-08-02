from PIL import Image
from GuiTools.handImage import handoToJpgStackedH, handToJpgV, handoToJpgStackedV


def renderGameState(gameState, trickHistory):
    HEIGHT = 768
    WIDTH = 768
    PADDING = 50
    COLOUR = (0, 153, 0, 0)

    hRATIO = int(200 / 1530)

    img = Image.new('RGB', (WIDTH, HEIGHT), color=COLOUR)

    # handImages
    handS = handoToJpgStackedH(gameState['playersHands'][0])
    handN = handoToJpgStackedH(gameState['playersHands'][2])
    handW = handoToJpgStackedH(gameState['playersHands'][1])
    handO = handoToJpgStackedH(gameState['playersHands'][3])
    # resize
    handS.thumbnail((450, 170))
    handW.thumbnail((450, 170))
    handN.thumbnail((450, 170))
    handO.thumbnail((450, 170))

    handW = handW.transpose(Image.ROTATE_90)
    handO = handO.transpose(Image.ROTATE_270)
    handN = handN.transpose(Image.ROTATE_180)

    # Pasting hands to image
    img.paste(handN, (int(WIDTH / 2) - int(handN.width / 2), 0 + PADDING))
    img.paste(handS, (int(WIDTH / 2) - int(handS.width / 2), HEIGHT - PADDING - handS.height))
    img.paste(handW, (0 + PADDING, int(HEIGHT / 2) - int(handW.height / 2)))
    img.paste(handO, (WIDTH - handO.width - PADDING, int(HEIGHT / 2) - int(handO.height / 2)))
    return img
