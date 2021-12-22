import cv2 as cv
import numpy as np

from Utilities import getMacroblocks, getBestResult

vid = cv.VideoCapture('../videos/video_1.mp4')  # Apothikeuoyme tin pliroforia tou video kai to prwto kai deutero
# plaisio

_, previousFrame = vid.read()
_, nextFrame = vid.read()

frames = np.concatenate((previousFrame, nextFrame), axis=0)
cv.imshow('Prwto kai Deutero plaisio', frames)

# Pernoume ola ta macroblocks apo ta duo plaisia
previousMacroblock = getMacroblocks(previousFrame)
nextMacroblock = getMacroblocks(nextFrame)


for row, macroblocks in enumerate(nextMacroblock):  # Ekteloume loop mesa apo kathe macroblock sto deutero plaisio
    for col, macroblock in enumerate(macroblocks):
        match = getBestResult(previousMacroblock, row, col, macroblock)  # Vriskoume to macroblock pou tairiazei
        # kalitera apo to proigoumeno plaisio

        absoluteDifference = cv.absdiff(macroblock, match)  # I apoliti diafora metaksi tou progoumenou kai epemenou
        # macroblock
        padded = cv.copyMakeBorder(macroblock, 0, 0, 0, 5, cv.BORDER_CONSTANT, value=[255, 255, 255])
        matchPadded = cv.copyMakeBorder(macroblock, 0, 0, 0, 5, cv.BORDER_CONSTANT, value=[255, 255, 255])
        image = np.concatenate((padded, matchPadded, absoluteDifference), axis=1)

        cv.imshow('To kalitero Macroblock', image)

        cv.waitKey(15)

vid.release()
cv.destroyAllWindows()
