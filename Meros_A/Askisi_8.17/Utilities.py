import numpy as np


def getMacroblocks(frame, window=16):
    oldWidth = frame.shape[0]
    width = resize(oldWidth)
    oldHeight = frame.shape[1]
    height = resize(oldHeight)

    widthPad = (0, width - oldWidth)
    heightPad = (0, height - oldHeight)
    depthPad = (0, 0)
    padding = (widthPad, heightPad, depthPad)

    paddedFrame = np.pad(frame, padding, mode='constant')

    macroblocks = []

    for width_ in range(0, width - window, window):
        row = []
        for height_ in range(0, height - window, window):
            macroblock = paddedFrame[width_:width_ + window, height_:height_ + window]
            row.append(macroblock)
        macroblocks.append(row)

    return macroblocks


def resize(x, window=16):
    return (x + window) - (x % window)


def getSAD(previousMacroblock, nextMacroblock,
           window=16):  # Athrisma apolitwn diaforwn me orismata to proigoumeno, epomeno macroblock kai to fixed size twn 16 block
    value = 0

    for i in range(window):  # Efarmozoume loop gia ola ta pixels enos plaisiou
        for j in range(window):
            # Pernoume tin pliroforia RGB gia ta dyo pixels
            previousPixel = previousMacroblock[i, j]
            nextPixel = nextMacroblock[i, j]

            for k in range(3):  # Vriskoume tin apoliti diafora gia ola ta tria xrwmata
                previousColor = int(previousPixel[k])
                nextColor = int(nextPixel[k])
                value += abs(nextColor - previousColor)

    return value


def getBestResult(previousMacroblock, nextRow, nextColumn, nextMacroblock,
                  k=16):  # Logarithmiki anazitisi gia tin texniki tis antistathmefsis kinisis
    pivot = k / 2  # Ksekiname apo tin mesi
    result = None  # Arxikopioisi

    while pivot != 1:  # Gia kathe vima vriskoume olous tous 8 kontinous geitones ean ta indexes einai egkira
        neighbours = []

        try:
            neighbours.append([nextRow + 1, nextColumn + 1, previousMacroblock[nextRow + 1][nextColumn + 1]])
        except IndexError:
            pass

        try:
            neighbours.append([nextRow + 1, nextColumn - 1, previousMacroblock[nextRow + 1][nextColumn - 1]])
        except IndexError:
            pass

        try:
            neighbours.append([nextRow - 1, nextColumn + 1, previousMacroblock[nextRow - 1][nextColumn + 1]])
        except IndexError:
            pass

        try:
            neighbours.append([nextRow - 1, nextColumn - 1, previousMacroblock[nextRow - 1][nextColumn - 1]])
        except IndexError:
            pass

        try:
            neighbours.append([nextRow + 1, nextColumn, previousMacroblock[nextRow + 1][nextColumn]])
        except IndexError:
            pass

        try:
            neighbours.append([nextRow, nextColumn - 1, previousMacroblock[nextRow][nextColumn - 1]])
        except IndexError:
            pass

        try:
            neighbours.append([nextRow, nextColumn + 1, previousMacroblock[nextRow][nextColumn + 1]])
        except IndexError:
            pass

        try:
            neighbours.append([nextRow - 1, nextColumn, previousMacroblock[nextRow - 1][nextColumn]])
        except IndexError:
            pass

        sadValues = [getSAD(neighbour[2], nextMacroblock) for neighbour in neighbours]  # Vriskoume ena geitoniko macroblock
        # me to kalitero sum of absolute difference
        sadMinimum = min(sadValues)

        minimumIndex = sadValues.index(sadMinimum)
        nextRow, nextColumn, nextMacroblock = neighbours[minimumIndex]

        pivot /= 2
        result = nextMacroblock

    return result
