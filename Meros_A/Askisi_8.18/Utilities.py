import numpy as np


def getMacroblocks(frame, window=16):
    # Pernoume to platos kai ypsos apo to frame gia na eksagoume ta macroblocks se ena sigkekrimeno megethos.
    oldWidth = frame.shape[0]
    width = resize(oldWidth)
    oldHeight = frame.shape[1]
    height = resize(oldHeight)

    # Vriskoyme ta blocks pou tha efarmosoume sto frame
    widthPad = (0, width - oldWidth)
    heightPad = (0, height - oldHeight)
    depthPad = (0, 0)
    padding = (widthPad, heightPad, depthPad)

    paddedFrame = np.pad(frame, padding, mode='constant')

    # Dimiourgoume 16x16 blocks me vasi to x-y tou frame.
    macroblocks = []

    for width_ in range(0, width - window, window):
        row = []
        for height_ in range(0, height - window, window):
            macroblock = paddedFrame[width_:width_ + window, height_:height_ + window]
            row.append(macroblock)
        macroblocks.append(row)

    # Epistrefoume tis grammes tou macroblock etsi oste to megethos na einai:
    # (arithmos grammwn, arithmos twn macroblocks, 16, 16, 3)
    return macroblocks


def getFrame(macroblocks):
    # Prwta prepei na synenwsoume ola ta macroblocks sto x plano gia kathe row.
    rows = []
    for row in macroblocks:
        rows.append(np.concatenate([macroblock for macroblock in row], axis=1))

    # Meta prepei na synenwsoume ola ta macroblocks sto y plano gia kathe row.
    frame = np.concatenate([row for row in rows], axis=0)

    # Epistrefoume to anakataskevasmeno plaisio poy diaferei apo to arxiko sxhma.
    return frame


def resize(x, window=16):
    # Vriskoume ton kontinotero integer me vasi to x poy diaireitai me 16
    return (x + window) - (x % window)
